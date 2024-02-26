const formatDate = (date) => {
    if (!date) return '';
    
    const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
    // The date is already in YYYY-MM-DD format for 'en-CA' locale
    return date.toLocaleDateString('en-CA', options);
  };

export {formatDate};