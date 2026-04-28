/**
 * Formats a number as Kenyan Shillings (KES)
 * @param {number} amount - The amount to format
 * @param {boolean} useSymbol - If true, uses "KSh" instead of "KES"
 * @returns {string} Formatted currency string
 */
export const formatKES = (amount, useSymbol = false) => {
  if (amount === undefined || amount === null) return useSymbol ? "KSh 0.00" : "KES 0.00";
  
  const formatted = new Intl.NumberFormat("en-KE", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);
  
  return useSymbol ? `KSh ${formatted}` : `KES ${formatted}`;
};

export default formatKES;