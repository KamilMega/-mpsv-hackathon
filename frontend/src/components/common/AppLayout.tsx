import { Outlet } from "react-router-dom";
import logo from "../../assets/img/mpsv-logo.png";
import logoWhite from "../../assets/img/mpsv-logo-white.png";
import { GovButton, GovIcon } from "@gov-design-system-ce/react";

export const AppLayout = () => {
  return (
    <>
      <div className="border-b border-[#C8D1E0]">
        <div className="flex justify-end text-primary-700 gov-container">
          <a href="#" className="bg-[#ebebeb] px-4 py-3 font-bold">
            MPSV
          </a>
          <a href="#" className="hover:bg-[#f3f3f3] px-4 py-3">
            Úřad práce
          </a>
          <a href="#" className="hover:bg-[#f3f3f3] px-4 py-3">
            ČSSZ
          </a>
          <a href="#" className="hover:bg-[#f3f3f3] px-4 py-3">
            SÚIP
          </a>
          <a href="#" className="hover:bg-[#f3f3f3] px-4 py-3">
            Další portály
          </a>
        </div>
      </div>

      <div className="flex items-center justify-between gov-container my-4">
        <div className="flex items-center space-x-4">
          <div
            style={{
              backgroundImage: `url(${logo})`,
              backgroundRepeat: "no-repeat",
              backgroundPosition: "center",
              backgroundSize: "contain",
            }}
            className="h-16 w-16"
          />
          <span className="font-bold text-primary-700">
            MINISTERSTVO PRÁCE
            <br />A SOCIÁLNÍCH VĚCÍ
          </span>
        </div>
        <div className="flex items-center">
          <GovButton type="base" color="primary" size="l">
            <GovIcon name="search" />
            Vyhledat
          </GovButton>
          <GovButton type="base" color="primary" size="l">
            Přihlásit se
          </GovButton>
          <GovButton type="base" color="primary" size="l">
            CZ
            <GovIcon name="chevron-down" />
          </GovButton>
        </div>
      </div>

      <div className="gov-container">
        <div className="bg-primary-700 flex items-center rounded-m p-3">
          <GovButton
            className="flex items-center"
            type="solid"
            color="primary"
            size="l"
          >
            <span className="font-medium">Průvodce</span>
            <GovIcon name="chevron-down" />
          </GovButton>
          <GovButton
            className="flex items-center"
            type="solid"
            color="primary"
            size="l"
          >
            <span className="font-medium">Ministerstvo</span>
            <GovIcon name="chevron-down" />
          </GovButton>
          <GovButton
            className="flex items-center"
            type="solid"
            color="primary"
            size="l"
          >
            <span className="font-medium">Působnost MPSV</span>
            <GovIcon name="chevron-down" />
          </GovButton>
          <GovButton type="solid" color="primary" size="l">
            <span className="font-medium">Formuláře</span>
          </GovButton>
          <GovButton type="solid" color="primary" size="l">
            <span className="font-medium">Kontakty</span>
          </GovButton>
        </div>
      </div>
      <div className={"pt-[38px] min-h-screen [ print:pt-0 ]"}>
        <Outlet />
      </div>
      <div className="gov-container flex flex-col mt-28 mb-16">
        <div className="bg-primary-700 flex rounded-m-nudge text-neutral-white px-12 py-16">
          <div className="w-1/4 flex-col">
            <div className="flex items-center space-x-4">
              <div
                style={{
                  backgroundImage: `url(${logoWhite})`,
                  backgroundRepeat: "no-repeat",
                  backgroundPosition: "center",
                  backgroundSize: "contain",
                }}
                className="h-12 w-12"
              />
              <span className="font-bold text-neutral-white text-xs">
                MINISTERSTVO PRÁCE
                <br />A SOCIÁLNÍCH VĚCÍ
              </span>
            </div>
          </div>
          <div className="w-1/4 flex flex-col text-sm">
            <div className="text-xl font-medium mb-2">Co je nového</div>
            <a className="my-1" href="">
              Aktuality
            </a>
            <a className="my-1" href="">
              Pro média
            </a>
            <a className="my-1" href="">
              Možnost přihlašování
            </a>
          </div>

          <div className="w-1/4 flex flex-col text-sm">
            <div className="text-xl font-medium mb-2">MPSV</div>
            <a className="my-1" href="">
              Ministerstvo
            </a>
            <a className="my-1" href="">
              Působnost MPSV
            </a>
            <a className="my-1" href="">
              Formuláře
            </a>
            <a className="my-1" href="">
              Kontakty
            </a>
          </div>

          <div className="w-1/4 flex flex-col text-sm">
            <div className="text-xl font-medium mb-2">Další portály</div>
            <a className="my-1" href="">
              Jenda - klientská zóna
            </a>
            <a className="my-1" href="">
              Úřad práce ČR
            </a>
            <a className="my-1" href="">
              Česká správa sociálního zabezpečení
            </a>
            <a className="my-1" href="">
              Státní úřad inspekce práce
            </a>
            <a className="my-1" href="">
              Operační program Zaměstnanost
            </a>
          </div>
        </div>
        <div className="flex justify-center space-x-4 my-10">
          <a className="w-12 h-12 rounded-full border-2 border-[#4669B0] flex justify-center items-center">
            FB
          </a>
          <a className="w-12 h-12 rounded-full border-2 border-[#000000] flex justify-center items-center">
            X
          </a>
          <a className="w-12 h-12 rounded-full border-2 border-[#FB201E] flex justify-center items-center">
            YT
          </a>
          <a className="w-12 h-12 rounded-full border-2 border-[#D63A75] flex justify-center items-center">
            IG
          </a>
        </div>
        <div className="flex justify-center space-x-10 text-sm text-primary">
          <a className="hover:underline" href="">
            Prohlášení o přístupnosti
          </a>
          <a className="hover:underline" href="">
            Mapa stránek
          </a>
          <a className="hover:underline" href="">
            GDPR
          </a>
        </div>
      </div>
    </>
  );
};
