const { test, expect } = require('@playwright/test');

test.describe('Kelli & Nathan Wedding Website Tests', () => {
  
  test.beforeEach(async ({ page }) => {
    // Load the wedding site from the test server
    await page.goto('/');
  });

  test('should load the home page with correct title', async ({ page }) => {
    await expect(page).toHaveTitle('Kelli & Nathan - September 10, 2027');
  });

  test('should display hero section with names and date', async ({ page }) => {
    // Check couple names
    const heroHeading = page.locator('#hero h1.couple-names');
    await expect(heroHeading).toContainText('Kelli & Nathan');
    
    // Check wedding date
    await expect(page.locator('#hero .wedding-date')).toContainText('September 10, 2027');
    
    // Check save the date text
    await expect(page.locator('#hero .save-the-date')).toContainText('Save the Date');
  });

  test('should display countdown timer', async ({ page }) => {
    const countdown = page.locator('#countdown');
    await expect(countdown).toBeVisible();
    
    // Countdown should contain time units
    await expect(countdown).toContainText('Days');
    await expect(countdown).toContainText('Hours');
    await expect(countdown).toContainText('Minutes');
    await expect(countdown).toContainText('Seconds');
  });

  test('should display all main navigation links', async ({ page }) => {
    // Check navigation links
    await expect(page.locator('nav a[href="#story"]')).toBeVisible();
    await expect(page.locator('a[href="#event"]')).toBeVisible();
    await expect(page.locator('a[href="#rsvp"]')).toBeVisible();
    await expect(page.locator('a[href="#gallery"]')).toBeVisible();
    await expect(page.locator('a[href="#registry"]')).toBeVisible();
  });

  test('should display Our Love Story timeline', async ({ page }) => {
    await page.locator('#story').scrollIntoViewIfNeeded();
    
    // Check timeline heading
    await expect(page.locator('#story h2')).toContainText('Our Love Story');
    
    // Check timeline items exist
    const timelineItems = page.locator('.timeline-item');
    await expect(timelineItems).toHaveCount(4);
    
    // Check years
    await expect(page.locator('.timeline-item .year').nth(0)).toContainText('2022');
    await expect(page.locator('.timeline-item .year').nth(1)).toContainText('2024');
    await expect(page.locator('.timeline-item .year').nth(2)).toContainText('2026');
    await expect(page.locator('.timeline-item .year').nth(3)).toContainText('2027');
  });

  test('should display event details section', async ({ page }) => {
    await page.locator('#event').scrollIntoViewIfNeeded();
    
    // Check section heading
    await expect(page.locator('#event h2')).toContainText('Wedding Details');
    
    // Check ceremony card
    await expect(page.locator('.card h3').filter({ hasText: 'Ceremony' })).toBeVisible();
    await expect(page.locator('.card').filter({ hasText: 'Ceremony' })).toContainText('September 10, 2027');
    await expect(page.locator('.card').filter({ hasText: 'Ceremony' })).toContainText('3:00 PM');
    
    // Check reception card
    await expect(page.locator('.card h3').filter({ hasText: 'Reception' })).toBeVisible();
    await expect(page.locator('.card').filter({ hasText: 'Reception' })).toContainText('September 10, 2027');
    await expect(page.locator('.card').filter({ hasText: 'Reception' })).toContainText('6:00 PM');
  });

  test('should have Add to Calendar button', async ({ page }) => {
    await page.locator('#event').scrollIntoViewIfNeeded();
    
    const addToCalendarBtn = page.locator('button').filter({ hasText: 'Add to Calendar' });
    await expect(addToCalendarBtn).toBeVisible();
  });

  test('should have View Location button', async ({ page }) => {
    await page.locator('#event').scrollIntoViewIfNeeded();
    
    const viewLocationBtn = page.locator('button').filter({ hasText: 'View Location' });
    await expect(viewLocationBtn).toBeVisible();
  });

  test('should display RSVP form with all fields', async ({ page }) => {
    await page.locator('#rsvp').scrollIntoViewIfNeeded();
    
    // Check section heading
    await expect(page.locator('#rsvp h2')).toContainText('RSVP');
    
    // Check form fields
    await expect(page.locator('#rsvpForm #name')).toBeVisible();
    await expect(page.locator('#rsvpForm #email')).toBeVisible();
    await expect(page.locator('#rsvpForm #attendance')).toBeVisible();
    await expect(page.locator('#rsvpForm #guests')).toBeVisible();
    await expect(page.locator('#rsvpForm #message')).toBeVisible();
    
    // Check submit button
    await expect(page.locator('#rsvpForm button[type="submit"]')).toBeVisible();
  });

  test('should fill and submit RSVP form', async ({ page }) => {
    await page.locator('#rsvp').scrollIntoViewIfNeeded();
    
    // Fill out the form
    await page.locator('#name').fill('Test Guest');
    await page.locator('#email').fill('test@example.com');
    await page.locator('#attendance').selectOption('yes');
    await page.locator('#guests').fill('2');
    await page.locator('#message').fill('Looking forward to the celebration!');
    
    // Submit the form
    await page.locator('#rsvpForm button[type="submit"]').click();
    
    // Check success message appears
    const successMessage = page.locator('#rsvpMessage');
    await expect(successMessage).toBeVisible();
    await expect(successMessage).toContainText('Thank you');
  });

  test('should display gallery section', async ({ page }) => {
    await page.locator('#gallery').scrollIntoViewIfNeeded();
    
    // Check section heading
    await expect(page.locator('#gallery h2')).toContainText('Our Memories');
    
    // Check photo grid exists
    const photoItems = page.locator('.photo-grid .photo-item');
    await expect(photoItems).toHaveCount(4);
  });

  test('should display registry section', async ({ page }) => {
    await page.locator('#registry').scrollIntoViewIfNeeded();
    
    // Check section heading
    await expect(page.locator('#registry h2')).toContainText('Gift Registry');
    
    // Check registry links
    await expect(page.locator('a.registry-card').filter({ hasText: 'Amazon' })).toBeVisible();
    await expect(page.locator('a.registry-card').filter({ hasText: 'Target' })).toBeVisible();
    await expect(page.locator('a.registry-card').filter({ hasText: 'Honeymoon' })).toBeVisible();
  });

  test('should have working navigation anchors', async ({ page }) => {
    // Click story link
    await page.locator('nav a[href="#story"]').click();
    await page.waitForTimeout(500);
    await expect(page.locator('#story')).toBeInViewport();
    
    // Click event link
    await page.locator('a[href="#event"]').click();
    await page.waitForTimeout(500);
    await expect(page.locator('#event')).toBeInViewport();
    
    // Click RSVP link
    await page.locator('a[href="#rsvp"]').click();
    await page.waitForTimeout(500);
    await expect(page.locator('#rsvp')).toBeInViewport();
  });

  test('should be responsive on mobile devices', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    
    // Check main elements are visible
    await expect(page.locator('#hero h1')).toBeVisible();
    await expect(page.locator('#countdown')).toBeVisible();
    await expect(page.locator('#navbar')).toBeVisible();
  });

  test('should be responsive on tablet devices', async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    
    // Check layout adapts
    await expect(page.locator('#hero h1')).toBeVisible();
    await expect(page.locator('.event-cards')).toBeVisible();
  });

  test('countdown should show positive days until September 10, 2027', async ({ page }) => {
    const countdownText = await page.locator('#countdown').textContent();
    
    // Extract days number
    const daysMatch = countdownText.match(/(\d+)\s*Days/);
    expect(daysMatch).toBeTruthy();
    
    const days = parseInt(daysMatch[1]);
    expect(days).toBeGreaterThan(0); // Should be positive (future date)
  });
});
