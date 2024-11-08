import { GovAccordion, GovAccordionItem } from "@gov-design-system-ce/react";

export const VolnaMistaFilters = () => {
  return (
    <div className="flex flex-col">
      <div className="text-2xl font-bold text-primary mb-6">Rozšířené hledání</div>
      <GovAccordion>
        <GovAccordionItem>
          <div slot="label">Obor</div>
          <div>to be done</div>
        </GovAccordionItem>
        <GovAccordionItem>
          <div slot="label">Region</div>
          <div>to be done</div>
        </GovAccordionItem>
        <GovAccordionItem>
          <div slot="label">Minimální stupeň vzdělání</div>
          <div>to be done</div>
        </GovAccordionItem>
      </GovAccordion>
    </div>
  );
};
