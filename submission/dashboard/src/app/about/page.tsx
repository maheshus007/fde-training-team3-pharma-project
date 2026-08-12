import { FadeIn } from "@/components/motion/fade-in";
import { glossary } from "@/lib/glossary";

const READING_STEPS = [
  "Read the decision state (e.g. Conditional-Go) as a governance signal for leadership, never as a regulated decision made by the system.",
  "Use the risk heatmap and evidence gaps to target accountable human review and follow-up, not to auto-resolve findings.",
  "Interpret value and cost metrics alongside their controls: lower cost or faster lead-time never removes human oversight of regulated decisions.",
  "When a workflow shows an abstention or a blocked action, treat it as the system working correctly, not as a failure.",
];

export default function AboutPage() {
  return (
    <div className="space-y-6">
      <FadeIn>
        <div>
          <h1 className="text-3xl font-semibold">Glossary &amp; reading guide</h1>
          <p className="mt-2 text-muted-foreground">
            Terms and reading conventions used across the AEGIS-PHARMA decision-support dashboard.
          </p>
        </div>
      </FadeIn>

      <FadeIn delay={0.05}>
        <section className="grid gap-4 md:grid-cols-2">
          {Object.entries(glossary).map(([term, meaning]) => (
            <article key={term} className="rounded-2xl border bg-card p-5">
              <h2 className="font-semibold text-primary">{term}</h2>
              <p className="mt-2 text-sm text-muted-foreground">{meaning}</p>
            </article>
          ))}
        </section>
      </FadeIn>

      <FadeIn delay={0.1}>
        <section className="rounded-2xl border bg-card p-5">
          <h2 className="font-semibold">How to read this dashboard</h2>
          <ol className="mt-3 list-decimal space-y-2 pl-5 text-sm text-muted-foreground">
            {READING_STEPS.map((step) => (
              <li key={step}>{step}</li>
            ))}
          </ol>
        </section>
      </FadeIn>
    </div>
  );
}
