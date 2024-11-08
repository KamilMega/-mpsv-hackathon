import { useRouteError } from "react-router-dom";

export default function ErrorPage() {
  const error = useRouteError();
  console.error(error);

  return (
    <div id="error-page">
      <div className="w-screen h-[calc(100vh-4.5rem)] flex flex-col items-center justify-center space-y-8">
        <h1 className="text-8xl">Oops!</h1>
        <p className="text-4xl">Sorry, an unexpected error has occured.</p>
      </div>
    </div>
  );
}
