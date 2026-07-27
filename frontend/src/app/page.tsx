import { Button } from "@/components/ui/button";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-orange-50 via-white to-amber-50">
      <section className="mx-auto flex min-h-screen max-w-7xl flex-col items-center justify-center px-6 text-center">
        <p className="mb-3 rounded-full bg-orange-100 px-4 py-1 text-sm font-medium text-orange-700">
          🛕 Smart Temple Management Platform
        </p>

        <h1 className="max-w-4xl text-5xl font-extrabold tracking-tight text-gray-900 md:text-7xl">
          Vishwaarpana Havihi
        </h1>

        <p className="mt-6 max-w-3xl text-lg leading-8 text-gray-600 md:text-xl">
          A modern digital platform for Temple Management, Online Pooja Booking,
          Priest Scheduling, Donations, Kundli Services, Catering, AI Assistance,
          and Multilingual Support in English & Kannada.
        </p>

        <div className="mt-10 flex flex-wrap justify-center gap-4">
          <Button size="lg">
            Book a Pooja
          </Button>

          <Button variant="outline" size="lg">
            Admin Login
          </Button>
        </div>

        <div className="mt-20 grid w-full max-w-6xl gap-6 md:grid-cols-3">
          <div className="rounded-2xl border bg-white p-8 shadow-sm">
            <h2 className="text-xl font-semibold">
              🛕 Temple Management
            </h2>

            <p className="mt-3 text-gray-600">
              Manage temples, priests, poojas, categories and schedules from one dashboard.
            </p>
          </div>

          <div className="rounded-2xl border bg-white p-8 shadow-sm">
            <h2 className="text-xl font-semibold">
              📅 Online Booking
            </h2>

            <p className="mt-3 text-gray-600">
              Users can book rituals, make secure payments and download invoices instantly.
            </p>
          </div>

          <div className="rounded-2xl border bg-white p-8 shadow-sm">
            <h2 className="text-xl font-semibold">
              🤖 AI Assistant
            </h2>

            <p className="mt-3 text-gray-600">
              Integrated AI helps devotees with pooja guidance, rituals and temple information.
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}