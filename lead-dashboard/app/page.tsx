export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <header className="border-b border-slate-800">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
          <p className="text-xl font-black tracking-wide text-amber-400">
            POWER ELECTRIC
          </p>
          <a
            className="rounded-md bg-amber-400 px-4 py-2 text-sm font-bold text-slate-950"
            href="tel:+15555555555"
          >
            Call (555) 555-5555
          </a>
        </div>
      </header>

      <section className="mx-auto grid max-w-6xl gap-12 px-6 py-20 md:grid-cols-2 md:items-center">
        <div>
          <p className="mb-5 text-sm font-bold tracking-widest text-amber-400">
            LICENSED ELECTRICAL SERVICES
          </p>
          <h1 className="text-5xl font-black leading-tight md:text-6xl">
            Power you can count on.
          </h1>
          <p className="mt-6 max-w-xl text-lg leading-8 text-slate-300">
            Power Electric delivers dependable residential and commercial
            electrical work, from quick repairs to complete upgrades.
          </p>
          <div className="mt-8 flex flex-wrap gap-4">
            <a
              className="rounded-md bg-amber-400 px-6 py-3 font-bold text-slate-950"
              href="tel:+15555555555"
            >
              Request Service
            </a>
            <a
              className="rounded-md border border-slate-600 px-6 py-3 font-bold"
              href="#services"
            >
              View Services
            </a>
          </div>
        </div>

        <div className="border border-slate-700 bg-slate-900 p-8">
          <p className="text-sm font-bold tracking-widest text-amber-400">
            AVAILABLE FOR
          </p>
          <ul className="mt-6 space-y-5 text-xl font-semibold">
            <li>Electrical repairs</li>
            <li>Panel upgrades</li>
            <li>Lighting installation</li>
            <li>Commercial electrical work</li>
          </ul>
        </div>
      </section>

      <section id="services" className="border-y border-slate-800 bg-slate-900">
        <div className="mx-auto max-w-6xl px-6 py-16">
          <p className="text-sm font-bold tracking-widest text-amber-400">
            OUR SERVICES
          </p>
          <h2 className="mt-3 text-3xl font-black">Electrical work, done right.</h2>
          <div className="mt-10 grid gap-4 md:grid-cols-3">
            {["Repairs", "Upgrades", "Installations"].map((service) => (
              <div key={service} className="border border-slate-700 p-6">
                <h3 className="text-xl font-bold">{service}</h3>
                <p className="mt-3 leading-7 text-slate-300">
                  Straightforward service from a qualified electrician.
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-6 py-16 text-center">
        <p className="text-sm font-bold tracking-widest text-amber-400">
          NEED AN ELECTRICIAN?
        </p>
        <h2 className="mt-3 text-3xl font-black">Call Power Electric today.</h2>
        <a
          className="mt-7 inline-block rounded-md bg-amber-400 px-6 py-3 font-bold text-slate-950"
          href="tel:+15555555555"
        >
          (555) 555-5555
        </a>
      </section>
    </main>
  );
}