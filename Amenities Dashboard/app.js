let allData = [];
let dataTable;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadCSVData();
    setupEventListeners();
});

// Load CSV data
async function loadCSVData() {
    try {
        const response = await fetch('AMENITY_FINAL.csv');
        const csvText = await response.text();
        allData = parseCSV(csvText);
        
        initializeTable();
        updateStats();
    } catch (error) {
        console.error('Error loading CSV:', error);
        document.getElementById('tableBody').innerHTML = 
            '<tr><td colspan="8" class="text-center text-danger">Error loading data. Please ensure AMENITY_FINAL.csv is in the same directory.</td></tr>';
    }
}

// Helper function to parse CSV line with quoted field support
function parseCSVLine(line) {
    const result = [];
    let current = '';
    let insideQuotes = false;
    
    for (let i = 0; i < line.length; i++) {
        const char = line[i];
        const nextChar = line[i + 1];
        
        if (char === '"') {
            if (insideQuotes && nextChar === '"') {
                current += '"';
                i++;
            } else {
                insideQuotes = !insideQuotes;
            }
        } else if (char === ',' && !insideQuotes) {
            result.push(current.trim());
            current = '';
        } else {
            current += char;
        }
    }
    
    result.push(current.trim());
    return result;
}

// Parse CSV text - Proper CSV parser that handles quoted fields
function parseCSV(csvText) {
    const lines = csvText.trim().split('\n');
    const headers = parseCSVLine(lines[0]).map(h => h.trim());
    
    console.log('Headers:', headers);
    
    const data = [];
    
    for (let i = 1; i < lines.length; i++) {
        if (lines[i].trim() === '') continue;
        
        const obj = {};
        const currentline = parseCSVLine(lines[i]);
        
        for (let j = 0; j < headers.length && j < currentline.length; j++) {
            obj[headers[j]] = currentline[j];
        }
        data.push(obj);
    }
    
    return data;
}

// Initialize DataTable
function initializeTable() {
    const tableBody = document.getElementById('tableBody');
    tableBody.innerHTML = '';
    
    // Filter for only 2022 data
    const data2022 = allData.filter(row => row.date.includes('2022'));
    
    console.log('Total 2022 records:', data2022.length);
    if (data2022.length > 0) {
        console.log('Sample row:', data2022[0]);
        console.log('Available keys:', Object.keys(data2022[0]));
    }
    
    data2022.forEach(row => {
        const tr = document.createElement('tr');
        // Try to get location from the column
        const locationKey = Object.keys(row).find(key => key.includes('location') || key.includes('adm4'));
        const location = locationKey ? row[locationKey] : 'Unknown';
        
        tr.innerHTML = `
            <td>${row.date}</td>
            <td>${formatNumber(row.college_nearest)}</td>
            <td>${formatNumber(row.community_centre_nearest)}</td>
            <td>${formatNumber(row.school_nearest)}</td>
            <td>${formatNumber(row.shelter_nearest)}</td>
            <td>${formatNumber(row.town_hall_nearest)}</td>
            <td>${formatNumber(row.university_nearest)}</td>
            <td><strong>${location}</strong></td>
        `;
        tableBody.appendChild(tr);
    });
    
    // Initialize DataTable with features
    if (dataTable) {
        dataTable.destroy();
    }
    
    dataTable = $('#dataTable').DataTable({
        pageLength: 25,
        lengthMenu: [10, 25, 50, 100],
        order: [[7, 'asc']],
        language: {
            search: "Filter results:",
            lengthMenu: "Show _MENU_ entries"
        },
        dom: '<"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6"f>>rtip',
        responsive: true
    });
}

// Format numbers to 2 decimal places
function formatNumber(num) {
    const n = parseFloat(num);
    if (isNaN(n)) return '0';
    if (n === 0) return '<span class="badge bg-success">0</span>';
    return n.toFixed(2);
}

// Update statistics
function updateStats() {
    // Filter for only 2022 data
    const data2022 = allData.filter(row => row.date.includes('2022'));
    
    document.getElementById('totalRows').textContent = data2022.length.toLocaleString();
    
    document.getElementById('dateRange').textContent = '2022';
    
    const today = new Date().toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
    document.getElementById('lastUpdated').textContent = today;
}

// Setup event listeners
function setupEventListeners() {
    // Search functionality
    document.getElementById('searchInput').addEventListener('keyup', function() {
        if (dataTable) {
            dataTable.search(this.value).draw();
        }
    });
    
    // Reset button
    document.getElementById('resetBtn').addEventListener('click', function() {
        document.getElementById('searchInput').value = '';
        if (dataTable) {
            dataTable.search('').draw();
        }
    });
    
    // Export to CSV
    document.getElementById('exportBtn').addEventListener('click', function() {
        exportToCSV();
    });
}

// Export table to CSV
function exportToCSV() {
    let csv = 'date,college_nearest,community_centre_nearest,school_nearest,shelter_nearest,town_hall_nearest,university_nearest,location1.adm4_en\n';
    
    const rows = dataTable.$('tr', {"filter": "applied"});
    
    rows.each(function() {
        const cells = $(this).find('td');
        const row = [];
        cells.each(function(index) {
            const text = $(this).text().trim();
            // Remove badge HTML if present
            const cleanText = text.replace(/<[^>]*>/g, '');
            row.push('"' + cleanText.replace(/"/g, '""') + '"');
        });
        csv += row.join(',') + '\n';
    });
    
    const link = document.createElement('a');
    link.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csv);
    link.download = 'amenity_data_' + new Date().toISOString().split('T')[0] + '.csv';
    link.click();
}

// Add sorting capability on column headers (DataTables handles this)
// Add color coding for distance values
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        // Add visual indicators for high/low distances
        document.querySelectorAll('#dataTable tbody tr').forEach(row => {
            row.querySelectorAll('td').forEach((td, index) => {
                if (index > 0 && index < 7) {
                    const value = parseFloat(td.textContent);
                    if (value === 0) {
                        td.style.backgroundColor = '#d4edda';
                    } else if (value > 2000) {
                        td.style.backgroundColor = '#f8d7da';
                    }
                }
            });
        });
    }, 500);
});
