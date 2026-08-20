import {
  Callout,
  Card,
  CardBody,
  CardHeader,
  Divider,
  Grid,
  H1,
  H2,
  H3,
  Pill,
  Row,
  Stack,
  Stat,
  Table,
  Text,
  TodoListCard,
  useCanvasState,
  useHostTheme,
} from "cursor/canvas";

type TabId =
  | "verdict"
  | "users"
  | "tools"
  | "scenarios"
  | "method"
  | "rubric"
  | "plan";

const TABS: { id: TabId; label: string }[] = [
  { id: "verdict", label: "Verdict" },
  { id: "users", label: "User model" },
  { id: "tools", label: "Which AI" },
  { id: "scenarios", label: "Scenarios" },
  { id: "method", label: "Method" },
  { id: "rubric", label: "Rubric" },
  { id: "plan", label: "Two-week plan" },
];

export default function EdgibleBetaUxSimulation() {
  const theme = useHostTheme();
  const [tab, setTab] = useCanvasState<TabId>("tab", "verdict");

  return (
    <Stack gap={20}>
      <Stack gap={8}>
        <H1>Edgible early-access UX simulation</H1>
        <Text tone="secondary">
          A working plan for rehearsing invited-beta first-run before real
          users arrive — treating AI chat as part of the product, not a
          side channel.
        </Text>
      </Stack>

      <Row gap={24} wrap>
        <Stat value="Yes, with a correction" label="Does the thesis hold?" />
        <Stat value="2 defaults" label="ChatGPT + Cursor/Claude Code" />
        <Stat value="8" label="Job scenarios to run" />
        <Stat value="5–8" label="Human sessions to keep" />
      </Row>

      <Row gap={8} wrap>
        {TABS.map((item) => (
          <span key={item.id}>
            <Pill
              active={tab === item.id}
              onClick={() => setTab(item.id)}
            >
              {item.label}
            </Pill>
          </span>
        ))}
      </Row>

      {tab === "verdict" ? <Verdict themeKind={theme.kind} /> : null}
      {tab === "users" ? <Users /> : null}
      {tab === "tools" ? <Tools /> : null}
      {tab === "scenarios" ? <Scenarios /> : null}
      {tab === "method" ? <Method /> : null}
      {tab === "rubric" ? <Rubric /> : null}
      {tab === "plan" ? <Plan /> : null}
    </Stack>
  );
}

function Verdict({ themeKind }: { themeKind: string }) {
  return (
    <Stack gap={16}>
      <Callout tone="success" title="The core bet is right">
        Invited early-access users will mostly arrive already sold on
        self-hosting, with a use case in mind, and they will try to make
        Edgible work by talking to an AI tool. That is a better rehearsal
        model than “user reads the docs top to bottom.”
      </Callout>

      <Callout tone="warning" title="Simulate the compound journey, not AI instead of docs">
        People do not choose AI or docs. They paste the invite, a CLI error,
        or a YAML snippet into ChatGPT / Claude / Cursor, and the model
        either retrieves your docs, invents a neighboring product, or both.
        Docs still matter — as the ground truth the model can fetch, not as
        the thing you expect humans to browse.
      </Callout>

      <H2>Why this is especially true for Edgible</H2>
      <Text>
        The first-run surface is CLI + YAML + a Linux agent. That is exactly
        the shape people paste into an AI chat. And because Edgible is
        pre-launch, frontier models will not know it well. The dominant
        failure mode is not “user cannot find the docs.” It is “the model
        confidently describes Cloudflare Tunnel, Tailscale Funnel, Coolify,
        or CasaOS, and the user follows it.”
      </Text>

      <H2>Keep assumption 1, tighten it</H2>
      <Table
        headers={["Assumption", "Keep as", "Do not treat as"]}
        rows={[
          [
            "Users understand self-hosting",
            "They want owned hardware, dislike SaaS lock-in, and have a job in mind",
            "They are fluent in systemd, WireGuard, Caddy, CRD-style YAML, or TLS issuance",
          ],
          [
            "They have a use case",
            "The session starts from a job (private AI, publish compose, replace ngrok)",
            "They will explore the product as a catalog of features",
          ],
          [
            "They use AI more than docs",
            "First prompt is to an AI tool; docs are retrieved, pasted, or skipped",
            "Docs and the website can be neglected — they are the model’s corpus",
          ],
        ]}
        striped
      />

      <H2>What simulation can find vs what it cannot</H2>
      <Grid columns={2} gap={12}>
        <Card>
          <CardHeader>AI-as-user finds</CardHeader>
          <CardBody>
            <Text>
              Invented CLI flags and YAML keys. Confusion with adjacent
              products. Missing machine-readable schema. Error messages that
              cannot be pasted back into a chat. Docs the model cannot fetch
              or that contradict the CLI.
            </Text>
          </CardBody>
        </Card>
        <Card>
          <CardHeader>Only humans on real hardware find</CardHeader>
          <CardBody>
            <Text>
              Trust in curl | bash and sudo. Waiting 30–90s for a
              certificate. “Is my home network actually safe?” Ambiguous
              success (“health check OK” vs a URL that loads). Fatigue after
              the fifth YAML retry.
            </Text>
          </CardBody>
        </Card>
      </Grid>

      <Text size="small" tone="tertiary">
        Plan for invited beta rehearsal. Theme: {themeKind}. Not a substitute
        for the first real invitees.
      </Text>
    </Stack>
  );
}

function Users() {
  return (
    <Stack gap={16}>
      <H2>Model invited users as jobs, not as “technical vs not”</H2>
      <Text>
        Early access is already filtered. The useful split is what they are
        trying to get live on hardware they control — and how much of that
        stack they already run.
      </Text>

      <Table
        headers={["Job", "They already have", "Success looks like", "Likely first AI prompt"]}
        rows={[
          [
            "Private AI",
            "A GPU box or workstation, Ollama or similar, maybe already local-only",
            "Chat with their model from phone/laptop, prompts never leave the box",
            "How do I expose Ollama through Edgible with an API key?",
          ],
          [
            "Publish existing compose",
            "A docker-compose app that already runs on the LAN",
            "HTTPS URL to that same app, no port forwarding",
            "I have a compose stack on a Pi, how do I put it on Edgible?",
          ],
          [
            "Replace a tunnel",
            "ngrok, Cloudflare Tunnel, or Tailscale Funnel in production-ish use",
            "Same public URL habit, but TLS ends on their machine",
            "Is Edgible like Cloudflare Tunnel? Migrate this service.",
          ],
          [
            "Share with a small team",
            "An internal tool, client data they will not put in SaaS",
            "Staff can reach it; it is not a public open door",
            "How do I require auth so only my team can hit this hostname?",
          ],
          [
            "First public self-host",
            "Linux curiosity, a mini-PC, conceptual buy-in, little ops practice",
            "Any hello-world URL that is clearly served from their box",
            "I was invited to Edgible, walk me through setup on Ubuntu.",
          ],
        ]}
        striped
        rowTone={["info", "info", "warning", "info", "success"]}
      />

      <H3>Starting knowledge to encode in every brief</H3>
      <Text>
        They know why self-hosting is attractive. They may not know Edgible’s
        nouns: serving device, agent, stack, workload subtype (pre-existing vs
        docker-compose), generated hostname, auth modes. If the AI uses those
        nouns without defining them, the human will nod and then stall at the
        YAML file.
      </Text>

      <Callout tone="info" title="Invite copy is the first context window">
        The email and landing page are not just marketing. For an AI-first
        user they are the text that gets pasted into the chat. Write them so
        a model that has never seen Edgible can still start in the right
        product family: outbound tunnel, TLS on your hardware, declare an app
        in YAML, not an app-store NAS UI.
      </Callout>
    </Stack>
  );
}

function Tools() {
  return (
    <Stack gap={16}>
      <Callout tone="success" title="Assume two tools, because the journey switches">
        First contact is a browser chatbot. Execution is an IDE or CLI agent
        once they are writing YAML. Simulating only ChatGPT under-tests the
        people most likely to finish. Simulating only Cursor under-tests the
        homelabber who never opens an editor.
      </Callout>

      <H2>What invited users are actually likely to open</H2>
      <Text>
        Edgible’s invitees are not average consumers and not only professional
        software engineers. Treat “most likely” as a split by moment in the
        session, not as a single market-share winner.
      </Text>

      <Table
        headers={["Moment", "Most likely tool", "Why", "Simulation default"]}
        rows={[
          [
            "Invite in inbox, no terminal yet",
            "ChatGPT",
            "Still the default assistant (~half of chatbot usage; Gemini second, Claude third but over-indexed among technical users)",
            "ChatGPT Free (GPT-5.6 Luna), web search on",
          ],
          [
            "Stuck on a CLI error or YAML file",
            "Same chat, paste the error — or switch to Cursor / Claude Code",
            "Homelab / SMB users stay in the chat tab. People who already live in an editor will @ the YAML and let an agent run commands",
            "Keep ChatGPT for paste-loop; Cursor or Claude Code for agent-on-VM",
          ],
          [
            "They want the agent to just do it",
            "Cursor or Claude Code",
            "Among developers in 2026 these are the primary coding agents; Copilot is still widely installed but used more as completion than as a walkthrough",
            "One agent tool is enough — pick Cursor or Claude Code and freeze it",
          ],
        ]}
        striped
        rowTone={["info", "warning", "success"]}
      />

      <H2>What to run (and what to skip)</H2>
      <Table
        headers={["Tool", "Role in the rehearsal", "Do this"]}
        rows={[
          [
            "ChatGPT Free (Luna, search on)",
            "Default chatbot — first contact + error paste-loop",
            "Must. Blind + grounded. ~94% of ChatGPT users are Free; Plus overstates help",
          ],
          [
            "Cursor or Claude Code",
            "Default agent — YAML + sudo on a real box",
            "Must. Agent-on-VM condition. Do not run both unless a finding is tool-specific",
          ],
          [
            "Claude.ai",
            "Technical / privacy-leaning chat",
            "Should, one pass of S1 and S4, if ChatGPT grounded still hallucinates schema",
          ],
          [
            "Gemini",
            "Search-native chatbot, second in consumer share",
            "Nice. One grounded S1 if you care whether Google’s index of edgible.com is enough",
          ],
          [
            "GitHub Copilot",
            "Inline completion, not a product walkthrough",
            "Skip as a primary simulation tool",
          ],
          [
            "Local Ollama / private model",
            "Aligned with Edgible’s pitch, useless as a navigator of an unknown CLI",
            "Skip. They have not stood Edgible up yet; they will not use it to learn Edgible",
          ],
        ]}
        striped
        rowTone={["success", "success", "info", "neutral", "neutral", "danger"]}
      />

      <H2>ChatGPT Free vs Plus</H2>
      <Text>
        Assume Free. OpenAI has on the order of 50 million paying subscribers
        against ~900 million weekly users — about 5–6% pay. Technical people
        who pay for AI often pay for Cursor or Claude Code and keep ChatGPT
        on Free as the casual tab. “Invited self-hoster” does not imply
        ChatGPT Plus.
      </Text>

      <Table
        headers={["Capability that matters for Edgible", "Free (default)", "Plus / Sol (sensitivity only)"]}
        rows={[
          [
            "Everyday text chat",
            "Unlimited as of mid-August 2026 — a 45-minute walkthrough will not hit a message cap",
            "Same, plus higher tool limits",
          ],
          [
            "Find edgible.com / docs",
            "Web search is included and auto-triggers — this is the real grounded path",
            "Same search, usually more generous limits",
          ],
          [
            "Default model",
            "GPT-5.6 Luna — fast, weaker at schema-faithful YAML and multi-step recovery",
            "GPT-5.6 Sol — stronger reasoning; do not use as the default",
          ],
          [
            "Think / agent mode",
            "Limited Think; no agent mode — it can advise, not SSH and run",
            "Fuller Think; agent mode exists on paid — a different product",
          ],
          [
            "Paste a docs page or error",
            "Yes. File-upload library is capped (~500MB) and rate-limited; paste still works",
            "Larger uploads, fewer tool-limit interruptions",
          ],
        ]}
        striped
        rowTone={["success", "success", "warning", "danger", "info"]}
      />

      <Callout tone="warning" title="Free is sufficient to attempt first-run, not guaranteed to complete it">
        Free can search, read a quickstart, emit commands, and interpret a
        pasted error. That is enough for the human-plus-AI loop to exist.
        What Free often cannot do is stay faithful to Edgible’s YAML and CLI
        across a long recovery. If S1 fails on Free+search, that is a product
        and docs problem — do not “fix” the rehearsal by switching to Plus.
      </Callout>

      <Text>
        Run Plus/Sol once on S1 and S4 as a sensitivity check. If Free fails
        and Plus succeeds, the AI-first thesis only holds for paying ChatGPT
        users. Then either make the CLI and docs Luna-survivable, or stop
        betting onboarding on ChatGPT quality.
      </Text>

      <Callout tone="info" title="Human sessions should not be assigned a tool">
        Track B: let people use whatever they already use, and log plan
        (Free vs Plus) as well as product. That calibration is more valuable
        than forcing ChatGPT. If five of eight open Cursor unprompted, weight
        the agent track higher before beta.
      </Callout>
    </Stack>
  );
}

function Scenarios() {
  return (
    <Stack gap={16}>
      <H2>Run jobs, not feature tours</H2>
      <Text>
        Each scenario is a closed task on a clean Linux machine. Stop at the
        success criterion. Do not coach unless the protocol says the AI may
        fetch docs.
      </Text>

      <Table
        headers={["ID", "Task", "Hardware / starting point", "Done when", "Priority"]}
        columnAlign={["left", "left", "left", "left", "left"]}
        rows={[
          [
            "S1",
            "First public URL",
            "Empty Ubuntu box, invite email only",
            "Browser loads a page at an edgible.app hostname",
            "Must run",
          ],
          [
            "S2",
            "Existing listener",
            "App already bound on localhost:8080",
            "Same app reachable via Edgible HTTPS, process unchanged",
            "Must run",
          ],
          [
            "S3",
            "Docker Compose they already have",
            "Working compose project on disk",
            "Stack deploy publishes it; tear-down leaves it gone",
            "Must run",
          ],
          [
            "S4",
            "Private AI with API key",
            "Ollama (or stand-in) on a named GPU/workstation device",
            "Request without key fails; request with key returns a model response",
            "Must run",
          ],
          [
            "S5",
            "Custom domain",
            "S1 complete, user owns a DNS zone",
            "HTTPS works on their domain, cert managed",
            "Should run",
          ],
          [
            "S6",
            "Recovery after a bad YAML",
            "Invalid stack file, or device name mismatch",
            "Error is understood; corrected file deploys",
            "Must run",
          ],
          [
            "S7",
            "Agent / device health",
            "Agent stopped, or device renamed in their head",
            "edgible device health (or equivalent) explains what to do next",
            "Should run",
          ],
          [
            "S8",
            "Adjacent-product trap",
            "User prompt frames Edgible as Coolify, Umbrel, or Tailscale",
            "Path is corrected before they install the wrong mental model’s stack",
            "Must run (AI track)",
          ],
        ]}
        striped
        rowTone={[
          "success",
          "success",
          "success",
          "success",
          "neutral",
          "warning",
          "neutral",
          "danger",
        ]}
      />

      <H3>First-run path the scenarios walk</H3>
      <Table
        headers={["Step", "Product moment", "AI-first failure to watch"]}
        rows={[
          ["1", "Invite → account", "Model sends them to a guessed URL or a waitlist that is not the beta"],
          ["2", "curl install.sh | bash", "Refuse, or invent apt/npm/brew packages that do not exist"],
          ["3", "edgible auth login", "OAuth vs email flags hallucinated; session confusion"],
          ["4", "sudo agent install + start", "Wrong --type / --device-type; skip systemd; skip sudo"],
          ["5", "device health", "Treat CLI silence as success; never confirm the device is serving"],
          ["6", "Write app YAML", "Invent apiVersion/kind; confuse compose with pre-existing; wrong hostPort"],
          ["7", "stack deploy / status", "Poll too soon; ignore cert/route wait; invent kubectl-like commands"],
          ["8", "Open the hostname", "HTTP vs HTTPS; authModes none on something that should be keyed"],
        ]}
        striped
      />
    </Stack>
  );
}

function Method() {
  return (
    <Stack gap={16}>
      <H2>Two tracks, same scenarios</H2>
      <Text>
        Cheap AI runs find whether a motivated user plus a current model can
        even construct a valid path. A small human sample finds whether a
        real person will trust and finish that path on their own machine.
      </Text>

      <Grid columns={2} gap={12}>
        <Card>
          <CardHeader trailing={<Text size="small">High N, cheap</Text>}>
            Track A — AI as proxy user
          </CardHeader>
          <CardBody>
            <Text>
              Run each scenario under three conditions. Score with the rubric.
              Re-run after every docs, CLI help, or error-string change. This
              becomes a regression suite for “can an assistant onboard someone.”
            </Text>
          </CardBody>
        </Card>
        <Card>
          <CardHeader trailing={<Text size="small">Low N, expensive</Text>}>
            Track B — humans, AI allowed
          </CardHeader>
          <CardBody>
            <Text>
              Five to eight invited-like people. Give the job, not a script.
              Allow their usual AI tool. Do not forbid docs and do not force
              them. Observe the mix. Think-aloud. Stop at 45 minutes.
            </Text>
          </CardBody>
        </Card>
      </Grid>

      <H2>Three AI conditions (run all three)</H2>
      <Table
        headers={["Condition", "What the model sees", "Simulates", "What a failure means"]}
        rows={[
          [
            "Blind",
            "Product name + job + ‘I have a Linux mini-PC’",
            "User heard of Edgible and asked ChatGPT cold",
            "Website, invite, and CLI names are not distinctive enough to survive zero training data",
          ],
          [
            "Grounded",
            "Same brief + edgible.com + docs.edgible.com (fetch or paste)",
            "User who pastes the invite or says ‘read this’",
            "Docs are incomplete, contradictory, or unusable as a retrieval corpus",
          ],
          [
            "Agent on a VM",
            "Grounded + permission to run commands on a throwaway Linux VM",
            "Cursor / Claude Code user who lets the agent do it",
            "The happy path is not automatable; errors are not recoverable from the CLI",
          ],
        ]}
        striped
        rowTone={["danger", "info", "success"]}
      />

      <Callout tone="info" title="Map conditions to tools, not to ‘an AI’">
        Blind and grounded: ChatGPT Free (GPT-5.6 Luna, search on). Plus/Sol
        is a one-shot sensitivity run, not the default. Agent on a VM: Cursor
        or Claude Code — pick one and freeze it. Details are in the Which AI
        tab.
      </Callout>

      <Callout tone="warning" title="What this Cursor agent can run vs a true Free ChatGPT loop">
        It can play the human: browse edgible.com and docs, click signup, follow
        whatever ChatGPT Free actually says if that chat is open in the browser.
        It cannot be GPT-5.6 Luna, cannot forget this planning conversation, and
        cannot sudo on a home mini-PC unless you provide a throwaway machine.
        Highest-fidelity run from here: ChatGPT Free types the advice, this
        agent executes it in the browser and records every stall.
      </Callout>

      <H2>Split-brain run from this chat</H2>
      <Text>
        When ChatGPT Free is not in the loop, honor the same constraints with
        two roles. The weights will not be Luna. The rules can be.
      </Text>
      <Table
        headers={["Role", "Allowed", "Forbidden"]}
        rows={[
          [
            "Advisor (fresh subagent)",
            "Answer as a chatbot. Web search / fetch public URLs. One job prompt, no product briefing",
            "This planning chat, Edgible YAML/CLI knowledge, terminal, sudo, clicking the product, reading the repo",
          ],
          [
            "Human (this agent)",
            "Execute only the advisor’s last instruction in the browser. Paste back errors and screenshots as text",
            "Coaching the advisor, fixing YAML from memory, peeking at docs the advisor did not retrieve",
          ],
        ]}
        striped
        rowTone={["info", "success"]}
      />
      <Text>
        Use a faster model for the advisor, not GPT-5.6 Sol — Sol is the Plus
        sensitivity run. Blind = job prompt only. Grounded = job prompt plus
        “search edgible.com and docs.edgible.com.” Stop if the advisor invents
        another product, asks the human to open inbound ports, or hits 25 turns.
      </Text>

      <H3>Protocol for one AI run</H3>
      <Text>
        1. Freeze website, docs, CLI --help, install script, and two example
        YAML files. Record versions. 2. Paste a scenario brief with no extra
        coaching. 3. Let the model work until success, a 25-message cap, or
        it tells the user to do something you would not ship (open inbound
        ports, disable auth on private data, install a different product).
        4. Score immediately. 5. Save the full transcript tagged S# /
        condition / model / date.
      </Text>

      <H3>Protocol for one human session</H3>
      <Text>
        Recruiter pitch: “You were invited to try a self-hosting tool. Get
        this app onto a URL without opening a port on your router.” Provide a
        loaner mini-PC or a cloud VM that stands in for home hardware. They
        may use any AI. Facilitator speaks only to unstick the environment
        (broken VM), never the product. Capture first prompt, whether they
        opened docs, every command, and the moment they believed they were
        done — which is often earlier or later than the actual URL.
      </Text>

      <Callout tone="neutral" title="Founder dogfood is not Track B">
        You already know the nouns. Use a clean VM with an agent for Track A
        (condition 3), and reserve Track B for people who have never shipped
        an Edgible YAML file.
      </Callout>

      <Divider />

      <H2>What to freeze before the first run</H2>
      <Table
        headers={["Surface", "Why the AI-first user hits it"]}
        rows={[
          ["Invite email + account signup", "Pasted into the first prompt; guessed URLs fail here"],
          ["get.edgible.com install script", "Models will wrap, rewrite, or refuse curl | bash"],
          ["edgible --help and subcommand help", "The schema the model will scrape if docs 404"],
          ["docs quickstart + YAML examples", "Grounded condition’s only source of truth"],
          ["One hello-world YAML and one Ollama YAML", "Prevents the model from inventing apiVersion"],
          ["A doctor / health command if it exists", "Recovery scenarios live or die on this string"],
        ]}
        striped
      />
    </Stack>
  );
}

function Rubric() {
  return (
    <Stack gap={16}>
      <H2>Score the path, not the vibes</H2>
      <Text>
        Each scenario × condition gets one row. Binary outcomes first, then
        counts of specific failure types. Average later; do not start with a
        1–5 “ease of use” score.
      </Text>

      <Table
        headers={["Signal", "How to record", "Pass"]}
        rows={[
          ["Activation", "Account exists, CLI installed, agent running", "All three"],
          ["Time to first URL", "Minutes from first command to HTTP 200", "S1 target: under 15 on a healthy VM"],
          ["Human/AI interventions", "Count of times the user had to correct the model or guess", "0–2 on grounded; blind may be higher"],
          ["Hallucinated interface", "Invented flags, YAML keys, URLs, or other products", "Zero in grounded and agent conditions"],
          ["Wrong-path depth", "Steps taken before returning to a valid Edgible path", "Caught within 3 turns"],
          ["Recovery", "From a real CLI/YAML error to a successful retry", "Error text alone was enough"],
          ["Security miss", "authModes none on private data; inbound ports; skipping TLS", "None"],
          ["False completion", "User or model declared done without a working URL", "None"],
        ]}
        striped
        rowTone={[
          "success",
          "info",
          "info",
          "danger",
          "warning",
          "warning",
          "danger",
          "warning",
        ]}
      />

      <H3>Tag every finding to a fixable surface</H3>
      <Table
        headers={["Tag", "Example finding", "Typical fix"]}
        rows={[
          [
            "CLI",
            "Model invents edgible app publish",
            "Subcommands that match user language; init scaffolding; stricter --help",
          ],
          [
            "Schema",
            "apiVersion v1 vs v3; wrong workload type",
            "JSON schema + edgible stack validate with next-step hint",
          ],
          [
            "Docs corpus",
            "Grounded model still uses kubectl-like verbs",
            "llms.txt, canonical YAML, explicit ‘not Coolify / not Tailscale’ page",
          ],
          [
            "Errors",
            "Deploy fails, model retries the same YAML",
            "Errors that name the field, the device, and the command to run next",
          ],
          [
            "Invite / web",
            "Blind model cannot find signup or install URL",
            "Stable get.edgible.com / docs URLs in the invite; copy-paste starter prompt",
          ],
          [
            "Trust",
            "Human refuses curl | bash or sudo",
            "Checksum, explain-then-install, non-root agent path if you can afford it",
          ],
        ]}
        striped
      />

      <Callout tone="info" title="North-star for this rehearsal">
        A grounded model, and then an agent on a clean VM, can complete S1
        and S4 without a hallucinated interface. If that fails, invited
        humans will fail the same way — they will just take longer and blame
        themselves.
      </Callout>
    </Stack>
  );
}

function Plan() {
  return (
    <Stack gap={16}>
      <H2>A rehearsal you can finish before invites go out</H2>
      <Text>
        Do not wait for a perfect lab. Freeze what you have, run S1/S4/S8
        blind this week, and let those transcripts decide which docs and CLI
        strings to fix before a human ever sits down.
      </Text>

      <TodoListCard
        defaultExpanded
        todos={[
          {
            id: "freeze",
            content:
              "Freeze website, docs quickstart, install script, CLI help, hello-world YAML, Ollama YAML; record versions",
            status: "pending",
          },
          {
            id: "briefs",
            content:
              "Write the 8 scenario briefs as paste-ready prompts (job, hardware, constraints, stop condition)",
            status: "pending",
          },
          {
            id: "blind",
            content:
              "Run S1, S4, S8 blind in ChatGPT Free (Luna, search on); catalogue hallucinations and adjacent-product confusion",
            status: "pending",
          },
          {
            id: "grounded",
            content:
              "Re-run S1–S4 and S6 grounded in ChatGPT Free with search/docs; one Plus/Sol sensitivity pass on S1 and S4",
            status: "pending",
          },
          {
            id: "agent-vm",
            content:
              "Agent-on-VM in Cursor or Claude Code (pick one): complete S1 and S2 unattended on a throwaway Linux box; capture every command",
            status: "pending",
          },
          {
            id: "humans",
            content:
              "Five invited-like sessions (AI allowed): 2× first public URL, 2× existing compose, 1× private AI",
            status: "pending",
          },
          {
            id: "synth",
            content:
              "Tag findings CLI / schema / docs / errors / invite / trust; pick a P0 list that fits before beta",
            status: "pending",
          },
          {
            id: "instrument",
            content:
              "Instrument real beta with the same funnel: signup → CLI → healthy device → first hostname 200",
            status: "pending",
          },
        ]}
      />

      <H3>Suggested order of product work that simulation usually forces</H3>
      <Text>
        After the first blind runs you will likely want, in this order: a
        canonical “what Edgible is not” paragraph in the invite; a JSON
        schema and stack validate; error strings that mention the next
        command; a copy-paste AI starter prompt on the quickstart; then
        whatever trust issue humans hit on curl | bash. Resist building a
        wizard until S1 fails for humans after those four are in place.
      </Text>

      <Callout tone="warning" title="Do not skip the human sample">
        If time is short, cut S5 and S7, not Track B. An agent completing
        S1 on a VM does not prove a homelabber will sudo your installer on
        the machine under their desk.
      </Callout>

      <H2>OpenClaw</H2>
      <Text>
        Not the regression backbone. Optional later harness for the
        agent-onboarding eval only. Whole-lifecycle Edgible coverage belongs
        in boring CI: CLI against a lab, HTTP 200, device health, tear-down.
      </Text>
      <Table
        headers={["Use", "Verdict", "Why"]}
        rows={[
          [
            "Product lifecycle regression (install → deploy → recover → teardown)",
            "No — use CI + VMs + CLI asserts",
            "Needs to be deterministic. Models make this flaky. OpenClaw would be an extra runtime to babysit",
          ],
          [
            "AI-onboarding eval: can an agent still complete S1/S4 after a docs/CLI change",
            "Optional, later",
            "Skills + YAML scenarios + transcripts fit. Same job can be a script that calls any agent. Use OpenClaw only if you already run it",
          ],
          [
            "Simulate ChatGPT Free first-run",
            "No, unless tools are stripped",
            "OpenClaw’s default is full system access. That is Cursor/Claude Code, not Luna-in-a-tab",
          ],
          [
            "Customer-facing ‘UX simulation product’",
            "No for beta",
            "That is a QA company. Invites should ship a self-hosting platform",
          ],
          [
            "OpenClaw itself hosted on Edgible",
            "Yes — better story",
            "Not ‘expose the dashboard to the world.’ Authenticated remote wss/https to a home Gateway — the job OpenClaw docs currently give to Tailscale Funnel",
          ],
        ]}
        striped
        rowTone={["danger", "info", "danger", "warning", "success"]}
      />
    </Stack>
  );
}
