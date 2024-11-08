import { GovChip, GovIcon, GovTag } from "@gov-design-system-ce/react";
import { Link } from "react-router-dom";
import { Listing } from ".";
import { formatNumber } from "../../helpers/formatNumber";

type VolneMistoTileProps = {
  listing: Listing;
};

export const VolneMistoTile = ({ listing }: VolneMistoTileProps) => {
  return (
    <div className="p-6 flex flex-col border border-[#C8D1E0] rounded-s-nudge space-y-4">
      <Link
        to={`/volna-mista/${listing.id}`}
        className="text-primary-700 font-bold text-[24px] hover:underline"
      >
        {listing.pozadovanaProfese}
      </Link>
      <GovTag type="subtle" color="secondary" size="m" className="max-w-fit">
        {listing.mesicniMzdaOd &&
          `od ${formatNumber(Number(listing.mesicniMzdaOd))}`}{" "}
        {listing.mesicniMzdaDo &&
          `do ${formatNumber(Number(listing.mesicniMzdaDo))}`}{" "}
        Kč/měsíc
      </GovTag>
      <div className="flex">
        <div className="text-[#212121] text-m py-2 pr-4 flex items-center space-x-2">
          <GovIcon
            type="complex"
            name="map"
            color="primary"
            size="xl"
          ></GovIcon>
          <span>
            {listing.obecNazev},{" "}
            {listing.okresNazev
              ? `okr. ${listing.okresNazev}`
              : listing.krajNazev}
          </span>
        </div>
        <div className="text-[#212121] text-m py-2 pr-4 flex items-center space-x-2">
          <GovIcon
            type="complex"
            name="cities"
            color="primary"
            size="xl"
          ></GovIcon>
          <span>{listing.nazevPracoviste}</span>
        </div>
        <div className="text-[#212121] text-m py-2 pr-4 flex items-center space-x-2">
          <GovIcon
            type="complex"
            name="graduate"
            color="primary"
            size="xl"
          ></GovIcon>
          <span>{listing.minPozadovaneVzdelaniNazev}</span>
        </div>
      </div>
      {listing.doporuceneKurzy.length > 0 && (
        <div className="flex flex-col p-4 rounded-s-nudge border border-secondary-200">
          <div className="flex justify-between items-center mb-5">
            <div className="text-lg font-medium text-text-primary">
              Související rekvalifikační kurzy{" "}
              <span className="font-normal">
                ({listing.doporuceneKurzy.length})
              </span>
            </div>
            <a className="text-primary font-bold underline">Zobrazit všechny</a>
          </div>
          <div className="flex flex-col divide-y divide-[#C8D1E0]">
            {/* Rekval listing */}
            {listing.doporuceneKurzy.map(
              (kurz, i) =>
                i < 3 && (
                  <div
                    key={kurz.id}
                    className="flex justify-between items-center space-x-4 py-2"
                  >
                    <div className="h-[38px] flex items-center">
                      {kurz.nazev}
                    </div>
                    {kurz.formaVyuky === "online" && (
                      <div className="flex flex-col justify-center">
                        <GovChip type="outlined" color="success">
                          Online
                        </GovChip>
                      </div>
                    )}
                  </div>
                )
            )}
          </div>
        </div>
      )}
    </div>
  );
};
