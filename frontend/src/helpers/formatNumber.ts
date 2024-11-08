export const formatNumber = (number: number) => {
  return new Intl.NumberFormat("en-US", {
    useGrouping: true,
  })
    .format(number)
    .replace(/,/g, "\u00A0");
};
