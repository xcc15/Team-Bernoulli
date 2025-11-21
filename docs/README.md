# Amenity Distance Data Viewer

An interactive web-based table viewer for amenity distance data. Displays distances from various locations to the nearest college, community center, school, shelter, town hall, and university.

## Features

✨ **Interactive Table**
- Sort columns by clicking headers
- Search/filter data across all columns
- Pagination with adjustable rows per page
- Responsive design for mobile devices

📊 **Data Analytics**
- Display total number of locations
- Show data date range
- Color-coded distance indicators
- Real-time filtering

📥 **Export Functionality**
- Download filtered data as CSV
- Reset filters with one click

## Setup for GitHub Pages

### Option 1: Deploy from `/docs` folder (Recommended)

1. Copy this webapp to a `docs` folder in your repository root:
   ```bash
   mkdir docs
   cp webapp/* docs/
   ```

2. Go to **Settings** → **Pages**
3. Select **Deploy from a branch**
4. Choose branch: `main`, folder: `/docs`
5. Your site will be available at: `https://xcc15.github.io/Team-Bernoulli/`

### Option 2: Deploy from root `/` folder

1. Move webapp files to repository root or keep in `/webapp` subfolder
2. Go to **Settings** → **Pages**
3. Choose branch: `main`, folder: `/` (or `/webapp`)
4. Your site will be live at the configured URL

### Option 3: Deploy from branch

1. Create a new branch `gh-pages`
2. Push all webapp files to that branch
3. Go to **Settings** → **Pages**
4. Select branch: `gh-pages`, folder: `/`

## File Structure

```
webapp/
├── index.html              # Main HTML file
├── app.js                  # JavaScript application logic
└── AMENITY_FINAL.csv       # Data file
```

## Local Testing

1. Start a local web server:
   ```bash
   python -m http.server 8000
   ```
   or
   ```bash
   python -m SimpleHTTPServer 8000
   ```

2. Open your browser to `http://localhost:8000`

## Data Format

CSV with columns:
- `date` - Date of record
- `college_nearest` - Distance to nearest college (meters)
- `community_centre_nearest` - Distance to nearest community center (meters)
- `school_nearest` - Distance to nearest school (meters)
- `shelter_nearest` - Distance to nearest shelter (meters)
- `town_hall_nearest` - Distance to nearest town hall (meters)
- `university_nearest` - Distance to nearest university (meters)
- `location1.adm4_en` - Location/Barangay name

## Customization

### Change Colors
Edit `style` section in `index.html`:
- `#667eea` - Primary purple
- `#764ba2` - Secondary purple

### Add Columns
Add new `<th>` in `index.html` and update JavaScript column mapping

### Adjust Table Size
Modify `pageLength: 25` in `app.js` to show more/fewer rows per page

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers

## Dependencies

- Bootstrap 5.3 (CSS Framework)
- Bootstrap Icons (Icon Library)
- DataTables 1.13 (Table functionality)
- jQuery 3.6 (JavaScript library)

All dependencies loaded from CDN - no installation required!

## Troubleshooting

**CSV not loading?**
- Ensure `AMENITY_FINAL.csv` is in the same directory as `index.html`
- Check browser console for errors (F12)
- CORS may block local file access - use a web server

**Table not displaying?**
- Clear browser cache (Ctrl+Shift+Delete)
- Check if JavaScript is enabled
- Verify CSV format is valid

## License

This project is part of the Team-Bernoulli repository.

## Questions?

For issues or improvements, please open an issue in the GitHub repository.
