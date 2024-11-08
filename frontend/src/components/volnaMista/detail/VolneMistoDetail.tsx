import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import apiClient from "../../../http-common";
import {
  GovButton,
  GovChip,
  GovIcon,
  GovLoading,
} from "@gov-design-system-ce/react";
import { AiBanner } from "../../common/AiBanner";
import { Listing } from "..";
import { formatNumber } from "../../../helpers/formatNumber";

export type Kurz = {
  dovednosti: string;
  formaVyuky: string;
  id: number;
  klicovaSlova: string;
  nazev: string;
  popis: string;
  relevance: number;
};

export const VolneMistoDetail = () => {
  const { id } = useParams();

  const useVolneMistoDetail = () =>
    useQuery({
      enabled: !!id,
      queryKey: ["volnaMista", id],
      queryFn: async () => {
        return await fetchVolneMistoDetail();
      },
      retry: 0,
    });

  const fetchVolneMistoDetail = async () => {
    return await apiClient.get<Listing>(`/volna-mista/${id}`);
  };

  const { data, isLoading } = useVolneMistoDetail();

  if (isLoading) return <GovLoading />;

  return (
    <div className="flex flex-col">
      <div className="gov-container flex flex-col">
        <div className="font-medium text-[40px] text-primary-700 mt-4 mb-8">
          {data?.data.pozadovanaProfese}
        </div>
        <div className="mb-14">
          <AiBanner
            title="Zaujala vás tato pozice? Pomůžeme vám ji získat!"
            description="Chcete tuto pozici? Řekněte nám, co umíte a my Vám poradíme co udělat pro to, abyste zvýšili pravděpodobnost získání této pozice."
            cta={
              <GovButton type="solid" color="primary">
                Zahájit chat
                <GovIcon type="complex" name="chat" size="xl" />
              </GovButton>
            }
          />
        </div>
      </div>
      <div className="flex justify-between space-x-16 gov-container">
        <div className="flex flex-col w-full space-y-8">
          <div className="border border-[#C8D1E0] flex flex-col rounded-m p-8 w-full space-y-6 text-text-primary">
            <div className="flex">
              <div className="flex flex-col w-1/3 text-sm">Zaměstnavatel</div>
              <div className="flex flex-col w-2/3">
                <div className="flex space-x-2">
                  <div className="flex flex-col">
                    <GovIcon
                      type="complex"
                      name="cities"
                      color="primary"
                      size="2xl"
                      className="mt-1"
                    />
                  </div>
                  <div className="flex flex-col">
                    <div className="text-lg">{data?.data.nazevPracoviste}</div>
                    <div className="text-sm text-[#616161]">
                      IČO: {data?.data.zamestnavatelIco}
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className="flex">
              <div className="flex flex-col w-1/3 text-sm">
                Místo výkonu práce
              </div>
              <div className="flex flex-col w-2/3 text-lg">
                <div className="flex space-x-2">
                  <div className="flex flex-col">
                    <GovIcon
                      type="complex"
                      name="map"
                      color="primary"
                      size="2xl"
                      className="mt-1"
                    />
                  </div>
                  <div className="flex flex-col">
                    <div>{data?.data.obecNazev}</div>
                    {!!data?.data.okresNazev && (
                      <div>okres {data?.data.okresNazev}</div>
                    )}
                    <div>{data?.data.krajNazev}</div>
                  </div>
                </div>
              </div>
            </div>
            <div className="flex">
              <div className="flex flex-col w-1/3 text-sm">Mzdové rozpětí</div>
              <div className="flex flex-col w-2/3 text-lg">
                <div className="flex space-x-2">
                  <div className="flex flex-col">
                    <GovIcon
                      type="complex"
                      name="coins"
                      color="primary"
                      size="2xl"
                      className="mt-1"
                    />
                  </div>
                  <div className="flex flex-col">
                    <div>
                      {!!data?.data.mesicniMzdaOd &&
                        `od ${formatNumber(
                          Number(data?.data.mesicniMzdaOd)
                        )}`}{" "}
                      {!!data?.data.mesicniMzdaDo &&
                        `do ${formatNumber(
                          Number(data?.data.mesicniMzdaDo)
                        )}`}{" "}
                      Kč/měsíc
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="border border-[#C8D1E0] flex flex-col rounded-m p-8 w-full divide-y divide-[#C8D1E0] text-text-primary text-lg">
            <div className="flex py-3 items-start">
              <div className="flex flex-col w-1/3 text-sm mt-1">
                Upřesňující informace
              </div>
              <div className="flex flex-col w-2/3 whitespace-pre-line">
                {data?.data.upresnujiciInformace}
              </div>
            </div>
            <div className="flex py-3 items-start">
              <div className="flex flex-col w-1/3 text-sm mt-1">
                Minimální stupeň vzdělání
              </div>
              <div className="flex flex-col w-2/3">
                {data?.data.minPozadovaneVzdelaniNazev}
              </div>
            </div>
            <div className="flex py-3 items-start">
              <div className="flex flex-col w-1/3 text-sm mt-1">
                Pracovněprávní vztah
              </div>
              <div className="flex flex-col w-2/3">
                {data?.data.pracovnePravniVztahNazev}
              </div>
            </div>
            <div className="flex py-3 items-start">
              <div className="flex flex-col w-1/3 text-sm mt-1">Dovednosti</div>
              <div className="flex flex-col w-2/3">{data?.data.dovednosti}</div>
            </div>
          </div>
        </div>
        <div className="p-8 flex flex-col space-y-4 bg-[#F5F5F5] rounded-m max-w-sm w-full h-fit text-text-primary">
          <div className="flex flex-col space-y-2">
            <div className="font-bold text-sm">Datum poslední změny:</div>
            <div>5. října 2024</div>
          </div>
          <div className="flex flex-col space-y-2">
            <div className="font-bold text-sm">Referenční číslo:</div>
            <div>14 069 500 704</div>
          </div>
        </div>
      </div>
      <div className="flex flex-col p-20 pr-0 bg-[#F5F5F5] mt-12">
        <div className="text-3xl text-primary font-bold mb-6">
          Související rekvalifikační kurzy{" "}
          <span className="font-normal">
            ({data?.data.doporuceneKurzy.length})
          </span>
        </div>
        <div className="flex space-x-6 overflow-x-auto">
          {data?.data.doporuceneKurzy.map((kurz) => (
            <div
              key={kurz.id}
              className="flex flex-col bg-neutral-white py-4 px-6 rounded-m min-w-[342px] space-y-2 h-[258px]"
            >
              <div className="text-primary text-xl font-medium text-ellipsis line-clamp-2">
                {kurz.nazev}
              </div>
              {kurz.formaVyuky === "online" && (
                <GovChip className="max-w-fit" type="outlined" color="success">
                  Online
                </GovChip>
              )}
              <div className="text-[#4F4F4F] text-ellipsis line-clamp-5">
                {kurz.popis}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
