import { VolnaMistaResponse } from "../components/volnaMista";

export const hasFiltersActive = (
  searchFilters: VolnaMistaResponse["searchFilters"]
) =>
  !!searchFilters?.lokace.nazev ||
  !!searchFilters?.minimalni_stupen_vzdelani ||
  !!searchFilters?.mzda.castka ||
  !!searchFilters?.mzda.jednotka ||
  !!searchFilters?.pracovnepravni_vztah;
