import {
  GovButton,
  GovFormInput,
  GovIcon,
  GovInfobar,
  GovLoading,
  GovPagination,
  GovTag,
} from "@gov-design-system-ce/react";
import { keepPreviousData, useQuery } from "@tanstack/react-query";
import { Controller, FormProvider, useForm } from "react-hook-form";
import { useSearchParams } from "react-router-dom";
import apiClient from "../../http-common";
import { VolneMistoTile } from "./VolneMistoTile";
import { VolnaMistaFilters } from "./VolnaMistaFilters";
import { useRef } from "react";
import { Kurz } from "./detail/VolneMistoDetail";
import { AiBanner } from "../common/AiBanner";
import { hasFiltersActive } from "../../helpers/hasFiltersActive";

const PAGE_SIZE = 10;

type VolnaMistaFormType = {
  query: string;
  page: number;
};

export type Listing = {
  doporuceneKurzy: Kurz[];
  distance: number;
  dovednosti: string;
  id: number;
  klicovaSlova: string;
  krajNazev: string;
  mesicniMzdaDo: string;
  mesicniMzdaOd: string;
  minPozadovaneVzdelaniNazev: string;
  nazevPracoviste: string;
  obecNazev: string;
  okresNazev: string;
  pozadovanaProfese: string;
  pracovnePravniVztahNazev: string;
  profeseCzIsco: number;
  upresnujiciInformace: string;
  zamestnavatelIco: string;
  zamestnavatelNazev: string;
};

export type VolnaMistaResponse = {
  results: Listing[];
  totalCount: number;
  searchFilters: {
    lokace: {
      nazev: string | null;
      typ: string | null;
    };
    minimalni_stupen_vzdelani: string | null;
    mzda: {
      castka: number | null;
      jednotka: string | null;
    };
    pracovnepravni_vztah: string | null;
  };
};

export const VolnaMista = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const defaultValues: VolnaMistaFormType = {
    query: searchParams.get("query") ?? "",
    page: 1,
  };
  const form = useForm({ defaultValues });

  const resultsRef = useRef<HTMLDivElement>(null);

  const current_page = form.watch("page");

  const useVolnaMistaResults = () =>
    useQuery({
      placeholderData: keepPreviousData,
      enabled: searchParams.toString().length > 0,
      queryKey: ["volnaMista", searchParams.toString()],
      queryFn: async () => {
        return await fetchVolnaMistaResults();
      },
      retry: 0,
    });

  const fetchVolnaMistaResults = async () => {
    return await apiClient.get<VolnaMistaResponse>(
      `/search?${searchParams.toString()}&pageSize=${PAGE_SIZE}`
    );
  };

  const { data, isLoading, isFetching } = useVolnaMistaResults();

  const searchFilters = data?.data.searchFilters;

  const handleSubmit = (formData: VolnaMistaFormType) => {
    setSearchParams({ query: formData.query, page: "1" });
  };

  return (
    <FormProvider {...form}>
      <form onSubmit={form.handleSubmit(handleSubmit)}>
        <div className="flex flex-col gov-container">
          <div className="font-medium text-[40px] text-primary-700 mt-4 mb-8">
            Hledání volných míst
          </div>
          <div className="p-10 -mx-10 bg-[#F5F5F5] rounded-m flex space-x-4 mb-8">
            <Controller
              name="query"
              render={({ field }) => (
                <GovFormInput
                  value={field.value}
                  onGovInput={(e) => field.onChange(e.target.value)}
                  placeholder="Hledám práci účetní na zkrácený úvazek v jihočeském kraji s platem od 40000Kč..."
                  className="relative"
                />
              )}
            />
            <GovButton
              type="outlined"
              color="neutral"
              onClick={() => setSearchParams(new URLSearchParams({}))}
            >
              Zrušit filtry
            </GovButton>
            <GovButton type="solid" color="secondary" nativeType="submit">
              Vyhledat
              <GovIcon name="search" />
            </GovButton>
          </div>

          {!!searchFilters && hasFiltersActive(searchFilters) && (
            <div className="flex flex-col mb-10 space-y-3">
              <div className="text-sm text-[#616161]">Vybrané filtry</div>
              <div className="flex space-x-2">
                {searchFilters.lokace.nazev && (
                  <GovTag type="bold" color="primary">
                    {searchFilters.lokace.nazev}
                    <GovIcon name="x" />
                  </GovTag>
                )}
                {searchFilters.minimalni_stupen_vzdelani && (
                  <GovTag type="bold" color="primary">
                    {searchFilters.minimalni_stupen_vzdelani}
                    <GovIcon name="x" />
                  </GovTag>
                )}
                {searchFilters.mzda.castka && (
                  <GovTag type="bold" color="primary">
                    {searchFilters.mzda.castka} {searchFilters.mzda.jednotka}
                    <GovIcon name="x" />
                  </GovTag>
                )}
                {searchFilters.pracovnepravni_vztah && (
                  <GovTag type="bold" color="primary">
                    {searchFilters.pracovnepravni_vztah}
                    <GovIcon name="x" />
                  </GovTag>
                )}
              </div>
            </div>
          )}

          <div className="mb-14">
            <AiBanner
              title="Potřebujete najít práci? Náš AI pomocník je tady pro vás!"
              description="Na základě údajů z popisu pracovní pozice vám doporučíme nabídky,
            které by vás mohly zajímat. Nabízíme taktéž možnost srovnání
            nabídek."
              cta={
                <GovButton type="solid" color="primary">
                  Začít výběr
                  <GovIcon name="search" />
                </GovButton>
              }
            />
          </div>

          <div className="flex space-x-4">
            <div className="flex flex-col max-w-sm w-1/4">
              <VolnaMistaFilters />
            </div>
            {isLoading ? (
              <GovLoading />
            ) : (
              !!data &&
              !!data.data && (
                <div
                  ref={resultsRef}
                  className="flex flex-col space-y-6 w-full h-full"
                >
                  {isFetching && <GovLoading />}
                  <div className="flex flex-col space-y-4">
                    {data.data.results.length === 0 ? (
                      <div className="flex justify-center items-center">
                        <GovInfobar
                          className="max-w-fit"
                          color="primary"
                          type="subtle"
                        >
                          Nebyly nalezeny žádné výsledky
                        </GovInfobar>
                      </div>
                    ) : (
                      data.data.results.map((result) => (
                        <VolneMistoTile key={result.id} listing={result} />
                      ))
                    )}
                  </div>
                  {data.data.results.length > 0 && (
                    <div className="flex justify-end">
                      <GovPagination
                        total={data.data.totalCount}
                        pageSize={PAGE_SIZE}
                        current={current_page}
                        onGovPage={(e) => {
                          const modifiedSearchParams = searchParams;
                          modifiedSearchParams.set(
                            "page",
                            e.detail.pagination.currentPage.toString()
                          );
                          setSearchParams(modifiedSearchParams);
                          resultsRef.current?.scrollIntoView({
                            behavior: "smooth",
                            block: "start",
                          });
                        }}
                      />
                    </div>
                  )}
                </div>
              )
            )}
          </div>
        </div>
      </form>
    </FormProvider>
  );
};
