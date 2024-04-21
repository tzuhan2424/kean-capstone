const formatDate = (date) => {
    if (!date) return '';
    
    const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
    // The date is already in YYYY-MM-DD format for 'en-CA' locale
    return date.toLocaleDateString('en-CA', options);
  };

const passDateCheck = (date) => {
    // Earliest date in database data
    const earliestDateInDB = { year: 1955, month: 1, day: 1 }

    // String must be valid and of format "YYYY-MM-DD", so the length is fixed to 10
    // and "-" characters must be in the expected positions
    if (date && (date.length === 10) && (date.indexOf('-') === 4) && (date.indexOf('-', 5) === 7)) {
      // Check if all other characters are digits (no fractions)
      for (const c of date) {
        if ((c !== '-') && ((c < '0') || (c > '9'))) {
          return false
        }
      }

      // Check date parameters
      const year = parseInt(date.substr(0,4))
      const month = parseInt(date.substr(5,2))
      const day = parseInt(date.substr(8,2))

      // Month should be within expected range
      if (month > 0 && month <= 12) {
        const numberOfDaysInMonths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        var numberOfDaysInMonth = numberOfDaysInMonths[month - 1]
        
        // Check for leap year and adjust number of days in February
        if ((month === 2) && (year % 4 === 0) && ((year % 400 === 0) || (year % 100 !== 0))) {
          numberOfDaysInMonth += 1
        }

        // Year should not exceed 3000 and day should be within expected range.
        // Overall date should also not be before the earliest in the database.
        return ((year <= 3000)
          && (day > 0) && (day <= numberOfDaysInMonth)
          && (year >= earliestDateInDB.year) && (month >= earliestDateInDB.month) && (day >= earliestDateInDB.day))
      }
    }

    // Return here if date is null or not of expected format
    return false
  }

const passDateRangeCheck = (fromDate, toDate) => {
    if (fromDate && toDate) {
      // Parse and get dates in milliseconds
      const fromDateMs = Date.parse(fromDate)
      const toDateMs = Date.parse(toDate)
  
      // If parsing fails, then NaN is returned. Check if from-date does not exceed to-date.
      return !isNaN(fromDateMs) && !isNaN(toDateMs) && (fromDateMs <= toDateMs)
    }

    return false
  }

export {formatDate, passDateCheck, passDateRangeCheck};

// Test cases for debugging
// console.log(passDateCheck('2024-02-26'))
// console.log(passDateCheck('1955-01-01'))
// console.log(passDateCheck('1954-12-31'))
// console.log(passDateCheck('0900-12-01'))
// console.log(passDateCheck('90.0-01-01'))
// console.log(passDateCheck('2000-13-01'))
// console.log(passDateCheck('800-12-01'))

// console.log(passDateRangeCheck('2023-12-31', '2024-01-01'))
// console.log(passDateRangeCheck('2024-01-01', '2024-01-01'))
// console.log(passDateRangeCheck('2024-01-02', '2024-01-01'))
// console.log(passDateRangeCheck('2024-01-02', '2024T01-01'))