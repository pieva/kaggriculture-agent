// Local browser verification of the rendered fragment, not Kaggle automation.
const fs = require('node:fs');
const path = require('node:path');
const {pathToFileURL} = require('node:url');
const {chromium} = require('C:/Users/pietr/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');

async function main() {
  const documentPath = path.resolve(process.argv[2]);
  const outputDir = path.dirname(documentPath);
  const browser = await chromium.launch({headless: true, channel: 'chrome'});
  const rows = [];
  try {
    for (const width of [360, 736, 1024]) {
      for (const colorScheme of ['light', 'dark']) {
        const page = await browser.newPage({viewport: {width: width + 32, height: 1050}, colorScheme});
        const errors = [];
        page.on('requestfailed', request => console.error('REQUEST FAILED', request.url(), request.failure()));
        page.on('console', message => { if (message.type() === 'error') console.error('BROWSER', message.text()); });
        page.on('pageerror', error => errors.push(error.message));
        await page.goto(pathToFileURL(documentPath).href);
        const frame = page.frameLocator('iframe');
        try {
          await frame.locator('svg.e30-plot').last().waitFor({timeout: 25000});
        } catch (error) {
          console.error('PAGE ERRORS', errors);
          throw error;
        }
        const root = frame.locator('#e30-top770-desktop-d30');
        const shape = await root.evaluate(el => ({
          width: el.getBoundingClientRect().width,
          panels: el.querySelectorAll('section[data-metric]').length,
          plots: el.querySelectorAll('svg.e30-plot').length,
          lines: el.querySelectorAll('[data-series-line]').length,
          points: el.querySelectorAll('path.point').length,
          overlaps: el.querySelectorAll('[data-label-overlap="true"]').length,
          overflow: el.scrollWidth > el.clientWidth + 1,
          columns: getComputedStyle(el.querySelector('.e30-grid')).gridTemplateColumns,
          minTextPx: Math.min(...[...el.querySelectorAll('svg text')].map(n => parseFloat(getComputedStyle(n).fontSize))),
          colors: [...el.querySelectorAll('[data-series-line]')].slice(0,2).map(n => getComputedStyle(n).stroke),
          badPoints: [...el.querySelectorAll('path.point')].filter(n => {
            const r = n.getBoundingClientRect();
            const f = n.closest('svg').querySelector('[data-chart-frame]').getBoundingClientRect();
            return r.x < f.x - .5 || r.y < f.y - .5 || r.right > f.right + .5 || r.bottom > f.bottom + .5;
          }).length,
        }));
        if (shape.panels !== 21 || shape.plots !== 21 || shape.lines !== 42 || shape.points !== 1260 || shape.overlaps || shape.overflow || shape.badPoints || shape.minTextPx < 11) {
          throw new Error(JSON.stringify({width, colorScheme, shape}));
        }
        const pass = frame.locator('section[data-metric="PASS"]');
        const hit = pass.locator('[data-chart-hit]');
        await hit.scrollIntoViewIfNeeded();
        await hit.hover({position: {x: 137, y: 60}});
        const tooltip = frame.locator('[role="tooltip"]');
        const tooltipText = await tooltip.innerText();
        if (!tooltipText.includes('Top770') || !tooltipText.includes('E18.30 V2')) throw new Error('Cross-series tooltip missing');
        if (await pass.locator('[data-chart-hover-marker]').count() !== 2) throw new Error('Missing hover marks');
        const candidate = frame.locator('button[data-series="candidate"]');
        await candidate.click();
        if (await candidate.getAttribute('aria-pressed') !== 'false') throw new Error('Legend toggle failed');
        if (await frame.locator('[data-series-group="candidate"][display="none"]').count() !== 21) throw new Error('Not all candidate marks hidden');
        await candidate.click();
        await hit.click({position: {x: 137, y: 60}});
        const pinned = await pass.locator('[data-chart-hover-guide]').getAttribute('x1');
        await hit.hover({position: {x: 157, y: 75}});
        if (await pass.locator('[data-chart-hover-guide]').getAttribute('x1') !== pinned) throw new Error('Pinned details moved');
        const hitBox = await hit.boundingBox();
        await page.mouse.click(hitBox.x + 157, hitBox.y + 75);
        if (errors.length) throw new Error(errors.join('\n'));
        if (width === 1024) {
          await pass.screenshot({path: path.join(outputDir, `e18-30-desktop-pass-${colorScheme}.png`)});
          await frame.locator('h2').scrollIntoViewIfNeeded();
          await page.screenshot({path: path.join(outputDir, `e18-30-desktop-overview-${colorScheme}.png`)});
        }
        rows.push({width, colorScheme, ...shape, tooltip: tooltipText, legend_toggle: true, pinned_details: true, page_errors: errors});
        console.log(JSON.stringify({width, colorScheme, passed: true}));
        await page.close();
      }
    }
  } finally {
    await browser.close();
  }
  const report = {passed: true, cases: rows, source: documentPath};
  fs.writeFileSync(path.join(outputDir, 'e18-30-desktop-qa.json'), JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report, null, 2));
}
main().catch(error => {console.error(error); process.exitCode = 1;});
