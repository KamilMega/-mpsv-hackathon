import banner from "../../assets/img/banner.png";
import { ReactNode } from "react";

type AiBannerProps = {
  title: string;
  description: string;
  cta: ReactNode;
};

export const AiBanner = ({ title, description, cta }: AiBannerProps) => {
  return (
    <div
      className="rounded-xl shadow-md"
      style={{ backgroundImage: "linear-gradient(to right, #FFD233, #FFF7C6)" }}
    >
      <div
        className="flex justify-evenly rounded-xl py-6 px-16 items-center space-x-6"
        style={{
          backgroundImage: `url(${banner})`,
          backgroundRepeat: "no-repeat",
          backgroundSize: "contain",
        }}
      >
        <div className="w-[250px]"></div>
        <div className="flex flex-col">
          <div className="text-[20px] font-bold">{title}</div>
          <div className="text-[16px]">{description}</div>
        </div>
        <div className="flex flex-col">{cta}</div>
      </div>
    </div>
  );
};
