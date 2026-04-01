# Mega Menu Implementation for Django PITAKA

## Overview

This document describes the complete mega menu implementation for the PITAKA Django project. The mega menu appears when hovering over navigation items and displays different content for each category.

## Architecture

### Files Modified/Created

1. **`templates/base.html`** - Updated header with navigation and mega menu include
2. **`templates/includes/mega_menu.html`** - Complete mega menu structure (NEW)
3. **`static/css/style.css`** - Added `.framed` and `.badge-new` styles
4. **`static/js/script.js`** - Contains mega menu JavaScript (already existed)

## Structure

### Navigation Items (`.nav-item`)

The navigation uses `data-menu` attributes to link nav items with mega menu sections:

```html
<nav class="nav">
    <div class="nav-item active" data-menu="phone">
        <span>Чехлы для телефонов</span>
    </div>
    <div class="nav-item" data-menu="tablet">
        <span>Чехлы для планшетов</span>
    </div>
    <div class="nav-item" data-menu="watch">
        <span>Аксессуары для Apple Watch и AirPods</span>
    </div>
    <div class="nav-item" data-menu="magsafe">
        <span>Аксессуары MagSafe</span>
    </div>
    <div class="nav-item" data-menu="accessories">
        <span>Аксессуары</span>
    </div>
</nav>
```

### Mega Menu Sections

Each section corresponds to a nav item via matching `data-menu` attribute:

```html
<div class="mega">
    <div class="mega-inner">
        <!-- PHONE SECTION -->
        <div class="mega-section active" data-menu="phone">
            <!-- Content with tabs: Devices, Series, Style -->
        </div>

        <!-- TABLET SECTION -->
        <div class="mega-section" data-menu="tablet">
            <!-- Content with tabs: Devices, Product Types -->
        </div>

        <!-- WATCH SECTION -->
        <div class="mega-section" data-menu="watch">
            <!-- Content with tabs: Bands, Aramid, AirPods -->
        </div>

        <!-- MAGSAFE SECTION -->
        <div class="mega-section" data-menu="magsafe">
            <!-- Content with tabs: Wallets, Powerbanks, Mounts -->
        </div>

        <!-- ACCESSORIES SECTION -->
        <div class="mega-section" data-menu="accessories">
            <!-- Content with tabs: Categories, Styles -->
        </div>
    </div>
</div>
```

## CSS Classes

### Core Mega Menu Classes

| Class | Purpose |
|-------|---------|
| `.mega` | Main container (fixed position, hidden by default) |
| `.mega.open` | Visible state with animation |
| `.mega-inner` | Centered content container (max-width: 1280px) |
| `.mega-section` | Individual section for each nav item |
| `.mega-section.active` | Currently visible section |
| `.mega-left` | Left sidebar with tabs |
| `.mega-content` | Content area (changes based on tab) |
| `.mega-content.active` | Currently visible content |
| `.mega-col` | Column within content area |
| `.mega-tab` | Clickable tab in left sidebar |
| `.mega-tab.active` | Active tab state |

### Product Display Classes

| Class | Purpose |
|-------|---------|
| `.framed` | White card with border for products |
| `.product-card` | Product image container |
| `.product-title` | Product name text |
| `.series-card` | Series display card |
| `.series-grid` | Grid layout for series cards |
| `.watch-grid` | Grid layout for watch products |
| `.style-grid` | Grid layout for style products |

### Interactive Classes

| Class | Purpose |
|-------|---------|
| `.model-item` | Clickable model link with hover underline |
| `.watch-link` | Watch/AirPods category link |
| `.style-link` | Style category link |
| `.badge-new` | Orange "NEW" badge |

## JavaScript Behavior

### Hover Interactions

```javascript
// When hovering over nav item:
1. Opens mega menu (.mega.open)
2. Activates corresponding nav item (.nav-item.active)
3. Shows matching section (.mega-section.active)
4. Auto-clicks first tab in section

// When hovering over mega menu:
- Stays open

// When leaving both nav and mega:
- Closes after 350ms delay
```

### Tab Switching

**Phone/Tablet Sections:**
- Click `.mega-tab` → Shows corresponding `.mega-content`
- Tabs: `data-tab="devices"`, `data-tab="series"`, `data-tab="style"`

**Watch/Magsafe Sections:**
- Click `.watch-link` → Shows corresponding `.watch-grid`
- Tabs: `data-watch="bands"`, `data-watch="aramid"`, `data-watch="airpods"`

**Style Content:**
- Click `.style-link` → Shows corresponding `.style-grid`
- Tabs: `data-style="moment"`, `data-style="essential"`, `data-style="collaboration"`

## Content Sections

### 1. Phone Section (`data-menu="phone"`)

**Tabs:**
- **По устройствам**: iPhone, Samsung, Google Pixel columns
- **По сериям**: UltraGuard, ProGuard, Ultra-Slim cards
- **По стилю**: Moment, Essential, Collaboration product grids

### 2. Tablet Section (`data-menu="tablet"`)

**Tabs:**
- **По устройствам**: iPad Pro, iPad Air, iPad Mini, iPad columns
- **По типу продукта**: Ultra-slim, Stand, Keyboard cases

### 3. Watch Section (`data-menu="watch"`)

**Tabs:**
- **Ремешки из карбона**: 6 watch band products
- **Чехлы из арамидного волокна**: 3 watch case products
- **Чехлы для AirPods**: 4 AirPods case products

### 4. MagSafe Section (`data-menu="magsafe"`)

**Tabs:**
- **Кардхолдер**: 3 wallet products
- **Повербанк**: 3 power bank products
- **Держатели и кольца**: 2 mount/grip products

### 5. Accessories Section (`data-menu="accessories"`)

**Tabs:**
- **По категориям**: Chargers, Grips, Wallets, Straps columns
- **По стилю**: Style-based product grid

## URL Integration

All links use Django `{% url %}` template tags:

```django
{# Model list URL #}
<a href="{% url 'catalog:model_list' 'iphone' 'iphone-17-pro-max' %}">
    iPhone 17 Pro Max
</a>

{# Catalog with filters #}
<a href="{% url 'catalog:catalog' %}?series=ultra-slim">
    Ultra-Slim
</a>
```

## Accessibility Features

1. **Keyboard Navigation**: ESC key closes mega menu
2. **Focus Management**: Returns focus to nav on close
3. **Touch Support**: Tap instead of hover on mobile
4. **Screen Reader**: Semantic HTML structure
5. **Reduced Motion**: Respects `prefers-reduced-motion`

## Responsive Behavior

### Desktop (> 1024px)
- Full mega menu with all tabs and columns
- Hover interactions enabled

### Tablet (768px - 1024px)
- Reduced padding and gaps
- Maintains structure

### Mobile (< 768px)
- Mega menu hidden (can be enhanced with mobile drawer)
- Navigation items become clickable instead of hover

## Performance Optimizations

1. **CSS Transitions**: Hardware-accelerated transforms
2. **Delayed Close**: 350ms prevents accidental closes
3. **Pointer Events**: Disabled when hidden
4. **Lazy Loading**: Images can be lazy-loaded

## Browser Support

- **Evergreen**: Chrome, Firefox, Edge, Safari (latest 2 versions)
- **Mobile**: iOS Safari 15+, Chrome Mobile
- **Fallback**: Graceful degradation for older browsers

## Testing Checklist

- [ ] Hover over each nav item shows correct section
- [ ] Tabs switch content correctly
- [ ] Mega menu closes when moving cursor away
- [ ] All links navigate to correct URLs
- [ ] Images load correctly
- [ ] Works on touch devices (tap to open)
- [ ] ESC key closes menu
- [ ] No JavaScript errors in console

## Common Issues & Solutions

### Issue: Mega menu doesn't open
**Solution**: Check that:
- `script.js` is loaded
- `.mega` element exists in DOM
- No JavaScript errors

### Issue: Wrong section shows
**Solution**: Verify `data-menu` attributes match between:
- `.nav-item[data-menu]`
- `.mega-section[data-menu]`

### Issue: Tabs don't switch
**Solution**: Check that:
- Tab has correct `data-tab` or `data-watch` or `data-style` attribute
- Target content has matching `id` or `data-*` attribute

## Future Enhancements

1. **Mobile Drawer**: Slide-out mega menu for mobile
2. **Search Integration**: Live search in mega menu
3. **Analytics**: Track popular categories
4. **Personalization**: Show recommended products
5. **Lazy Loading**: Load images on hover

## Contact

For questions or issues, refer to the project's main documentation.
