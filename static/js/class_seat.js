// Classroom Seating Grid Selection and Booking Logic

document.addEventListener('DOMContentLoaded', () => {
  // 1. Initialize data and state variables
  const classes = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th"];
  let selectedClass = null;
  let selectedSeat = null;

  // Make sure takenSeatsData is defined
  const takenSeatsData = window.takenSeatsData || {};

  // DOM elements
  const classPillsContainer = document.getElementById('class-pills');
  const seatGrid = document.getElementById('seat-grid');
  
  // Sidebar stats elements
  const infoClass = document.getElementById('info-class');
  const infoTotal = document.getElementById('info-total');
  const infoAvail = document.getElementById('info-avail');
  const infoTaken = document.getElementById('info-taken');
  const infoSeat = document.getElementById('info-seat');
  const barPct = document.getElementById('bar-pct');
  const availBar = document.getElementById('avail-bar');

  // Form elements
  const bookingForm = document.getElementById('booking-form');
  const fieldClass = document.getElementById('field-class');
  const fieldSeat = document.getElementById('field-seat');
  const seatChipWrap = document.getElementById('seat-chip-wrap');
  const bookBtn = document.getElementById('book-btn');
  const boardClassLabel = document.getElementById('board-class-label');

  // Ticket overlays
  const successOverlay = document.getElementById('success-overlay');

  // Render Class selector pills
  function renderClassPills() {
    classPillsContainer.innerHTML = '';
    classes.forEach(cls => {
      const takenSeats = takenSeatsData[cls] || [];
      const takenCount = takenSeats.length;
      const totalSeats = 30; // 5 rows x 6 columns
      const availCount = totalSeats - takenCount;
      
      const pill = document.createElement('div');
      pill.className = 'class-pill' + (selectedClass === cls ? ' active' : '') + (availCount === 0 ? ' full' : '');
      pill.dataset.class = cls;
      pill.innerHTML = `
        ${cls} Class
        <span class="avail">${availCount} seats left</span>
      `;
      
      if (availCount > 0) {
        pill.addEventListener('click', () => {
          selectClass(cls);
        });
      }
      classPillsContainer.appendChild(pill);
    });
  }

  // Handle Class selection
  function selectClass(cls) {
    selectedClass = cls;
    selectedSeat = null; // Clear seat selection when class changes
    
    // Update inputs
    fieldClass.value = cls;
    fieldSeat.value = '';
    
    // Clear seat selection chip
    seatChipWrap.innerHTML = '<div class="no-seat-msg"><i class="bi bi-cursor-fill me-1"></i>Click a seat on the map</div>';
    bookBtn.disabled = true;

    // Update Blackboard text
    boardClassLabel.textContent = `${cls} Grade Seating Plan`;

    // Render components
    renderClassPills();
    renderSeatGrid();
    updateStats();
  }

  // Render the Seating Grid (5 rows x 6 cols)
  function renderSeatGrid() {
    seatGrid.innerHTML = '';
    
    if (!selectedClass) {
      seatGrid.innerHTML = `
        <div style="text-align:center;padding:32px 20px;color:var(--ink-muted);font-size:14px;">
          <i class="bi bi-arrow-up-circle" style="font-size:28px;display:block;margin-bottom:8px;opacity:.4;"></i>
          Please select a class above to view available seats
        </div>
      `;
      return;
    }
    
    const takenSeats = takenSeatsData[selectedClass] || [];
    const rows = ['A', 'B', 'C', 'D', 'E'];
    const cols = [1, 2, 3, 4, 5, 6];
    
    rows.forEach(rowLetter => {
      const rowEl = document.createElement('div');
      rowEl.className = 'seat-row';
      
      // Add row letter label
      const labelEl = document.createElement('div');
      labelEl.className = 'row-label';
      labelEl.textContent = rowLetter;
      rowEl.appendChild(labelEl);
      
      // Render seats
      cols.forEach((colNum, colIndex) => {
        // Add a gap (aisle) in the center after the 3rd column
        if (colIndex === 3) {
          const gapEl = document.createElement('div');
          gapEl.className = 'seat-gap';
          rowEl.appendChild(gapEl);
        }
        
        const seatId = `${rowLetter}${colNum}`;
        const isTaken = takenSeats.includes(seatId);
        const isSelected = selectedSeat === seatId;
        
        const seatEl = document.createElement('div');
        seatEl.className = 'seat' + (isTaken ? ' taken' : '') + (isSelected ? ' selected' : '');
        seatEl.dataset.seat = seatId;
        
        seatEl.innerHTML = `
          <span class="seat-ico"><i class="bi bi-person"></i></span>
          <span class="seat-num">${seatId}</span>
        `;
        
        if (!isTaken) {
          seatEl.addEventListener('click', () => {
            selectSeat(seatId);
          });
        }
        rowEl.appendChild(seatEl);
      });
      
      seatGrid.appendChild(rowEl);
    });
  }

  // Handle Seat selection
  function selectSeat(seatId) {
    selectedSeat = seatId;
    fieldSeat.value = seatId;

    // Render grid to update selection styles
    renderSeatGrid();

    // Update form chip
    seatChipWrap.innerHTML = `
      <div class="selected-seat-chip">
        <i class="bi bi-check-circle-fill me-1"></i> Seat ${seatId}
      </div>
    `;

    // Enable Booking button
    bookBtn.disabled = false;

    // Update Stats sidebar
    updateStats();
  }

  // Update Sidebar statistics
  function updateStats() {
    if (!selectedClass) {
      infoClass.textContent = '—';
      infoTotal.textContent = '—';
      infoAvail.textContent = '—';
      infoTaken.textContent = '—';
      infoSeat.textContent = 'None';
      barPct.textContent = '0%';
      availBar.style.width = '0%';
      return;
    }

    const takenSeats = takenSeatsData[selectedClass] || [];
    const takenCount = takenSeats.length;
    const totalSeats = 30;
    const availCount = totalSeats - takenCount;
    const occupancyPct = Math.round((takenCount / totalSeats) * 100);

    infoClass.textContent = `${selectedClass} Class`;
    infoTotal.textContent = totalSeats;
    infoAvail.textContent = availCount;
    infoTaken.textContent = takenCount;
    infoSeat.textContent = selectedSeat || 'None';
    barPct.textContent = `${occupancyPct}%`;
    availBar.style.width = `${occupancyPct}%`;
  }

  // 2. Intercept Form Submission and perform AJAX post
  bookingForm.addEventListener('submit', (e) => {
    e.preventDefault();

    if (!selectedClass || !selectedSeat) {
      alert('Please select both a class and a seat.');
      return;
    }

    const formData = new FormData(bookingForm);
    
    // AJAX Request to the seat view
    fetch('', {
      method: 'POST',
      body: formData,
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      if (data.status === 'success') {
        // Populate the success ticket
        document.getElementById('t-class').textContent = `${data.class_grade} Class`;
        document.getElementById('t-seat').textContent = data.seat_number;
        document.getElementById('t-child').textContent = data.child_name;
        document.getElementById('t-parent').textContent = formData.get('parent_name');

        // Show Success Overlay
        successOverlay.classList.add('show');
      } else {
        alert('Booking failed: ' + (data.message || 'Unknown error'));
      }
    })
    .catch(err => {
      console.error('Error submitting booking:', err);
      alert('An error occurred during booking. Please try again.');
    });
  });

  // Export closeSuccess globally so the onclick works
  window.closeSuccess = function() {
    window.location.href = '/parent/';
  };

  // Initial render
  renderClassPills();
  updateStats();
});
