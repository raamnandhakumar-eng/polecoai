<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="The Frontline Exposure Gap: Evidence on AI Adoption in Retail and Service Occupations from Task-Level Usage Data, by Sriramkrishnan Nandhakumar.">
  <meta name="author" content="Sriramkrishnan Nandhakumar">
  <meta name="keywords" content="generative AI, frontline work, occupational exposure, task-level adoption, labor economics, Anthropic Economic Index">

  <meta property="og:type" content="article">
  <meta property="og:title" content="The Frontline Exposure Gap">
  <meta property="og:description" content="Frontline occupations account for 31.7% of U.S. employment but only 11.1% of task-matched AI usage.">
  <meta property="og:image" content="figures/fig1_representation.png">

  <title>The Frontline Exposure Gap | Sriramkrishnan Nandhakumar</title>

  <style>
    :root {
      --ink: #17211f;
      --muted: #5f6c69;
      --teal: #117c72;
      --teal-dark: #0b5f57;
      --teal-soft: #eaf6f4;
      --line: #dce4e2;
      --paper: #ffffff;
      --page: #f5f7f6;
      --code: #eef2f1;
      --shadow: 0 12px 32px rgba(22, 45, 41, 0.08);
    }

    * {
      box-sizing: border-box;
    }

    html {
      scroll-behavior: smooth;
    }

    body {
      margin: 0;
      background: var(--page);
      color: var(--ink);
      font-family: Georgia, "Times New Roman", serif;
      font-size: 18px;
      line-height: 1.68;
    }

    a {
      color: var(--teal-dark);
      text-decoration-thickness: 1px;
      text-underline-offset: 3px;
    }

    a:hover {
      color: var(--teal);
    }

    .topbar {
      position: sticky;
      top: 0;
      z-index: 20;
      border-bottom: 1px solid var(--line);
      background: rgba(255, 255, 255, 0.96);
      backdrop-filter: blur(10px);
    }

    .topbar-inner {
      width: min(1180px, calc(100% - 32px));
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 20px;
      min-height: 64px;
    }

    .brand {
      font-family: Arial, Helvetica, sans-serif;
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--ink);
      text-decoration: none;
      white-space: nowrap;
    }

    nav {
      display: flex;
      flex-wrap: wrap;
      justify-content: flex-end;
      gap: 18px;
      font-family: Arial, Helvetica, sans-serif;
      font-size: 0.83rem;
    }

    nav a {
      color: var(--muted);
      text-decoration: none;
    }

    nav a:hover {
      color: var(--teal-dark);
    }

    main {
      width: min(1180px, calc(100% - 32px));
      margin: 34px auto 64px;
    }

    .paper-card {
      overflow: hidden;
      border: 1px solid var(--line);
      border-radius: 18px;
      background: var(--paper);
      box-shadow: var(--shadow);
    }

    .hero {
      padding: clamp(34px, 6vw, 76px);
      border-bottom: 1px solid var(--line);
      background:
        radial-gradient(circle at top right, rgba(17, 124, 114, 0.11), transparent 38%),
        linear-gradient(180deg, #ffffff 0%, #fbfdfc 100%);
    }

    .eyebrow {
      margin: 0 0 14px;
      color: var(--teal-dark);
      font-family: Arial, Helvetica, sans-serif;
      font-size: 0.78rem;
      font-weight: 700;
      letter-spacing: 0.09em;
      text-transform: uppercase;
    }

    h1 {
      max-width: 980px;
      margin: 0;
      font-size: clamp(2.05rem, 5vw, 4.45rem);
      line-height: 1.08;
      letter-spacing: -0.035em;
    }

    .author-line {
      margin: 26px 0 0;
      color: var(--muted);
      font-family: Arial, Helvetica, sans-serif;
      font-size: 0.96rem;
      line-height: 1.7;
    }

    .author-line strong {
      color: var(--ink);
    }

    .tag-row {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 22px;
    }

    .tag {
      border: 1px solid #cfe3df;
      border-radius: 999px;
      padding: 6px 11px;
      background: var(--teal-soft);
      color: var(--teal-dark);
      font-family: Arial, Helvetica, sans-serif;
      font-size: 0.75rem;
      font-weight: 700;
    }

    .actions {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 30px;
    }

    .button {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 46px;
      border: 1px solid var(--teal-dark);
      border-radius: 9px;
      padding: 10px 16px;
      font-family: Arial, Helvetica, sans-serif;
      font-size: 0.86rem;
      font-weight: 700;
      text-decoration: none;
    }

    .button-primary {
      background: var(--teal-dark);
      color: #fff;
    }

    .button-primary:hover {
      background: var(--teal);
      color: #fff;
    }

    .button-secondary {
      background: #fff;
      color: var(--teal-dark);
    }

    .button-secondary:hover {
      background: var(--teal-soft);
    }

    .content-grid {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 270px;
      gap: 54px;
      padding: clamp(30px, 5vw, 66px);
    }

    article {
      min-width: 0;
    }

    aside {
      align-self: start;
      position: sticky;
      top: 92px;
    }

    aside .box {
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 18px;
      background: #fbfcfc;
      font-family: Arial, Helvetica, sans-serif;
      font-size: 0.78rem;
      line-height: 1.55;
    }

    aside h2 {
      margin-top: 0;
      font-size: 0.86rem;
      border: 0;
      padding: 0;
    }

    aside ul {
      margin: 0;
      padding-left: 18px;
    }

    aside li {
      margin: 8px 0;
    }

    section {
      scroll-margin-top: 88px;
    }

    section + section {
      margin-top: 58px;
    }

    h2 {
      margin: 0 0 18px;
      border-bottom: 1px solid var(--line);
      padding-bottom: 9px;
      font-size: clamp(1.42rem, 2.6vw, 2rem);
      line-height: 1.25;
    }

    h3 {
      margin: 30px 0 10px;
      font-size: 1.15rem;
      line-height: 1.35;
    }

    p {
      margin: 0 0 1.1em;
    }

    .lead {
      font-size: 1.08rem;
    }

    .stat-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
      margin: 24px 0 8px;
    }

    .stat {
      border: 1px solid var(--line);
      border-radius: 12px;
      padding: 20px;
      background: #fbfcfc;
    }

    .stat strong {
      display: block;
      margin-bottom: 4px;
      color: var(--teal-dark);
      font-family: Arial, Helvetica, sans-serif;
      font-size: 1.65rem;
      line-height: 1.1;
    }

    .stat span {
      color: var(--muted);
      font-family: Arial, Helvetica, sans-serif;
      font-size: 0.78rem;
      line-height: 1.45;
    }

    .findings {
      list-style: none;
      margin: 0;
      padding: 0;
      counter-reset: finding;
    }

    .findings li {
      counter-increment: finding;
      position: relative;
      margin: 0;
      padding: 20px 0 20px 54px;
      border-bottom: 1px solid var(--line);
    }

    .findings li::before {
      content: counter(finding);
      position: absolute;
      left: 0;
      top: 19px;
      width: 34px;
      height: 34px;
      border-radius: 50%;
      display: grid;
      place-items: center;
      background: var(--teal-soft);
      color: var(--teal-dark);
      font-family: Arial, Helvetica, sans-serif;
      font-size: 0.8rem;
      font-weight: 700;
    }

    .findings strong {
      color: var(--teal-dark);
    }

    figure {
      margin: 34px 0;
    }

    figure img {
      display: block;
      width: 100%;
      height: auto;
      border: 1px solid var(--line);
      border-radius: 10px;
      background: #fff;
    }

    figcaption {
      margin-top: 10px;
      color: var(--muted);
      font-family: Arial, Helvetica, sans-serif;
      font-size: 0.74rem;
      line-height: 1.5;
    }

    .formula {
      margin: 24px 0;
      border-left: 4px solid var(--teal);
      padding: 14px 18px;
      background: var(--teal-soft);
      font-size: 1.08rem;
      text-align: center;
    }

    .paper-frame {
      width: 100%;
      min-height: 760px;
      border: 1px solid var(--line);
      border-radius: 10px;
      background: #f8f9f9;
    }

    .note {
      border: 1px solid #cfe3df;
      border-radius: 10px;
      padding: 16px 18px;
      background: var(--teal-soft);
      font-family: Arial, Helvetica, sans-serif;
      font-size: 0.82rem;
      line-height: 1.55;
    }

    pre {
      overflow-x: auto;
      margin: 16px 0;
      border: 1px solid var(--line);
      border-radius: 10px;
      padding: 18px;
      background: var(--code);
      font-family: "SFMono-Regular", Consolas, "Liberation Mono", monospace;
      font-size: 0.76rem;
      line-height: 1.55;
      white-space: pre-wrap;
    }

    .copy-button {
      border: 1px solid var(--teal-dark);
      border-radius: 8px;
      padding: 8px 11px;
      background: #fff;
      color: var(--teal-dark);
      cursor: pointer;
      font-family: Arial, Helvetica, sans-serif;
      font-size: 0.76rem;
      font-weight: 700;
    }

    .copy-button:hover {
      background: var(--teal-soft);
    }

    .references {
      padding-left: 22px;
      font-size: 0.88rem;
    }

    .references li {
      margin: 12px 0;
    }

    footer {
      border-top: 1px solid var(--line);
      padding: 26px clamp(30px, 5vw, 66px);
      background: #fbfcfc;
      color: var(--muted);
      font-family: Arial, Helvetica, sans-serif;
      font-size: 0.76rem;
      line-height: 1.55;
    }

    @media (max-width: 900px) {
      .content-grid {
        grid-template-columns: 1fr;
      }

      aside {
        display: none;
      }
    }

    @media (max-width: 680px) {
      body {
        font-size: 17px;
      }

      .topbar-inner {
        align-items: flex-start;
        flex-direction: column;
        padding: 14px 0;
      }

      nav {
        justify-content: flex-start;
        gap: 12px;
      }

      .stat-grid {
        grid-template-columns: 1fr;
      }

      .hero,
      .content-grid {
        padding-left: 22px;
        padding-right: 22px;
      }

      .paper-frame {
        min-height: 560px;
      }
    }

    @media print {
      .topbar,
      .actions,
      aside,
      .copy-button,
      .paper-frame {
        display: none;
      }

      body,
      main,
      .paper-card {
        background: #fff;
        box-shadow: none;
      }

      main {
        width: 100%;
        margin: 0;
      }

      .paper-card {
        border: 0;
      }
    }
  </style>
</head>

<body>
  <header class="topbar">
    <div class="topbar-inner">
      <a class="brand" href="#top">The Frontline Exposure Gap</a>
      <nav aria-label="Primary navigation">
        <a href="#abstract">Abstract</a>
        <a href="#findings">Findings</a>
        <a href="#figures">Figures</a>
        <a href="#paper">Paper</a>
        <a href="#citation">Citation</a>
      </nav>
    </div>
  </header>

  <main id="top">
    <div class="paper-card">
      <header class="hero">
        <p class="eyebrow">Independent working paper · Revised July 2026</p>
        <h1>The Frontline Exposure Gap: Evidence on AI Adoption in Retail and Service Occupations from Task-Level Usage Data</h1>

        <p class="author-line">
          <strong>Sriramkrishnan Nandhakumar</strong><br>
          Boston University Questrom School of Business (MBA 2026)<br>
          <a href="mailto:raam.nandhakumar@gmail.com">raam.nandhakumar@gmail.com</a>
        </p>

        <div class="tag-row" aria-label="Paper metadata">
          <span class="tag">JEL J23</span>
          <span class="tag">JEL J24</span>
          <span class="tag">JEL O33</span>
          <span class="tag">Generative AI</span>
          <span class="tag">Labor markets</span>
          <span class="tag">Task-level adoption</span>
        </div>

        <div class="actions">
          <a class="button button-primary" href="paper/paper.pdf" target="_blank" rel="noopener">Read the paper (PDF)</a>
          <a class="button button-secondary" href="https://github.com/raamnandhakumar-eng/polecoai" target="_blank" rel="noopener">Replication materials</a>
        </div>
      </header>

      <div class="content-grid">
        <article>
          <section id="abstract">
            <h2>Abstract</h2>
            <p class="lead">
              This paper measures realized AI adoption in frontline service occupations using the Anthropic Economic Index, which maps millions of AI conversations to O*NET task statements. Frontline occupations in sales, office and administrative support, food preparation and serving, and personal care and service account for 31.7 percent of U.S. employment but only 11.1 percent of task-matched AI usage.
            </p>
            <p>
              Occupational classification understates this gap. Excluding technical occupations classified under clerical codes reduces the administrative-support representation index from 0.65 to 0.34, while a task-splitting robustness check leaves the estimates unchanged. Comparisons of the February and August 2025 releases provide suggestive evidence that the gap persisted rather than narrowed. Conditional on reaching frontline tasks, AI use is also more likely to involve automation-style interactions. In frontline administrative-support tasks, 62.7 percent of classified conversations are automation-style, compared with 43.0 percent in other occupations.
            </p>
            <p>
              Occupation-level regressions show that the gap is not primarily a wage gradient. The estimated wage elasticity of usage is 0.38 (robust SE = 0.19), and the coefficient on a frontline indicator is statistically indistinguishable from zero. February 2026 exposure scores further reveal polarization between screen-mediated and physically co-present service occupations. The paper discusses demand, access, organizational, and measurement mechanisms and their distributional implications.
            </p>

            <div class="stat-grid" aria-label="Headline results">
              <div class="stat">
                <strong>31.7%</strong>
                <span>Share of U.S. employment in the four frontline occupation groups.</span>
              </div>
              <div class="stat">
                <strong>11.1%</strong>
                <span>Share of task-matched AI usage attributed to those groups.</span>
              </div>
              <div class="stat">
                <strong>0.34</strong>
                <span>Corrected administrative-support representation index, down from 0.65.</span>
              </div>
              <div class="stat">
                <strong>62.7%</strong>
                <span>Automation-style share in frontline administrative-support usage.</span>
              </div>
            </div>
          </section>

          <section id="motivation">
            <h2>Motivation</h2>
            <p>
              While operating Krishna Foods and Energy, I observed a sharp divide between back-office tasks and work performed on the production and retail floor. Demand forecasts, supplier comparisons, pricing analyses, customer correspondence, and management reports could be digitized and increasingly supported by AI. Packing, stocking, serving customers, supervising production, and resolving real-time quality problems remained physical, time-sensitive, and difficult to mediate through a chat interface.
            </p>
            <p>
              The task-level data reproduce that practical divide. AI appears first in the information tasks embedded within frontline occupations, while the in-person core of the work remains largely absent. The central question is therefore not only where AI could be used, but where it is actually being used.
            </p>
          </section>

          <section id="method">
            <h2>Measurement and data</h2>
            <p>
              The analysis combines task-level usage from the Anthropic Economic Index with O*NET task statements, occupation codes, and wages, plus U.S. Bureau of Labor Statistics employment data. It also uses Anthropic's February 2026 occupation-level observed-exposure measure as a complementary cross-section.
            </p>

            <div class="formula" aria-label="Representation index formula">
              <em>Representation index</em> = occupation group's share of AI usage ÷ occupation group's share of employment
            </div>

            <p>
              A value of 1 indicates usage proportional to employment. Values below 1 indicate underrepresentation. The analysis is descriptive. It does not estimate a causal effect. Its main empirical focus is measurement validity across occupational classification, shared task mappings, small cells, and platform selection.
            </p>
          </section>

          <section id="findings">
            <h2>Main findings</h2>
            <ol class="findings">
              <li>
                <strong>Frontline occupations are deeply underrepresented.</strong> The four frontline groups account for 31.7 percent of employment but 11.1 percent of observed task-matched usage. Their representation indices range from 0.64 for office and administrative support to 0.06 for food preparation and serving, compared with 10.94 for computer and mathematical occupations.
              </li>
              <li>
                <strong>The raw administrative-support estimate is inflated by taxonomy.</strong> Excluding Bioinformatics Technicians, Computer Operators, Statistical Assistants, and Desktop Publishers reduces the administrative-support index from 0.645 to 0.338. Other frontline estimates change by no more than 0.01.
              </li>
              <li>
                <strong>Wages explain little of the cross-occupation pattern.</strong> Among 585 occupations with positive usage and wage data, the wage elasticity is 0.38 with a robust standard error of 0.19. The frontline indicator is statistically indistinguishable from zero. The regression is conditional on positive observed usage and does not fully identify the extensive margin.
              </li>
              <li>
                <strong>The 2025 releases show continued underrepresentation.</strong> Administrative support, sales, and personal care rise modestly between February and August 2025, while food service falls from 0.061 to 0.045. Because the releases use different classification pipelines and task universes, this is suggestive evidence rather than a formal trend estimate.
              </li>
              <li>
                <strong>Frontline usage is more automation-oriented.</strong> Automation-style interactions account for 62.7 percent of classified frontline administrative-support conversations, compared with 58.1 percent in computer and mathematical occupations and 43.0 percent in other occupations.
              </li>
              <li>
                <strong>Exposure is polarized within frontline work.</strong> In February 2026, 44 of 112 frontline occupations register zero observed exposure. Customer Service Representatives score 0.70, compared with 0.32 for Retail Salespersons and 0.08 for Cashiers. Screen-mediated service tasks show high coverage, while physically co-present work remains close to zero.
              </li>
            </ol>
          </section>

          <section id="figures">
            <h2>Selected figures</h2>

            <figure>
              <img src="figures/fig1_representation.png" alt="AI usage and employment shares across occupation groups" loading="lazy">
              <figcaption>
                Figure 1. AI usage and employment shares across SOC major groups. Bars show task-matched Claude conversation share; points show U.S. employment share. Source: Anthropic Economic Index and BLS OEWS.
              </figcaption>
            </figure>

            <figure>
              <img src="figures/fig4_temporal.png" alt="Representation indices in February and August 2025" loading="lazy">
              <figcaption>
                Figure 4. Representation indices in the February and August 2025 AEI releases. The comparison is descriptive because the releases use different classification pipelines and task universes.
              </figcaption>
            </figure>

            <figure>
              <img src="figures/fig5_automation_share.png" alt="Automation-style share of conversations by occupation group" loading="lazy">
              <figcaption>
                Figure 5. Automation-style share of classified conversations by occupation group. Automation combines directive and feedback-loop interaction modes.
              </figcaption>
            </figure>

            <figure>
              <img src="figures/fig6_exposure_2026.png" alt="Observed AI exposure by occupation in February 2026" loading="lazy">
              <figcaption>
                Figure 6. Observed AI exposure by occupation, February 2026. Dots represent occupations and vertical bars represent unweighted group means.
              </figcaption>
            </figure>
          </section>

          <section id="interpretation">
            <h2>Interpretation</h2>
            <h3>Demand and task medium</h3>
            <p>
              The in-person core of frontline work, including stocking, serving, de-escalating, and caring, cannot be performed easily through a language-model interface. This helps explain the near-zero coverage of food service and personal care and the divide between screen-mediated and physically co-present tasks.
            </p>

            <h3>Access and organizational complements</h3>
            <p>
              Frontline work often takes place under workplace time, device, permission, and workflow constraints. Even technically feasible tools may remain unused without employer-provided access, redesigned workflows, training, and worker-facing deployment.
            </p>

            <h3>Measurement</h3>
            <p>
              Claude usage is not representative of all AI usage, and employer-deployed systems are incompletely observed. Platform selection likely inflates the level of the measured gap. It is less able to explain the within-frontline polarization, taxonomy findings, or conditional interaction-mode differences.
            </p>
          </section>

          <section id="limitations">
            <h2>Limitations</h2>
            <ul>
              <li>The data capture Claude usage rather than all generative AI use.</li>
              <li>User occupation is inferred from task content rather than observed directly.</li>
              <li>Conversation share is not equivalent to work-time share or productivity.</li>
              <li>The February and August 2025 releases are not a methodologically consistent panel.</li>
              <li>Employer-deployed AI may be underrepresented in consumer conversation data.</li>
              <li>The February 2026 group means are unweighted across occupations unless detailed employment weights are supplied.</li>
            </ul>
          </section>

          <section id="paper">
            <h2>Full paper</h2>
            <p class="note">
              The embedded viewer uses <code>paper/paper.pdf</code>. Keep this HTML file at the repository root and keep the PDF at <code>paper/paper.pdf</code>.
            </p>

            <object class="paper-frame" data="paper/paper.pdf" type="application/pdf">
              <p>
                Your browser cannot display the embedded PDF.
                <a href="paper/paper.pdf" target="_blank" rel="noopener">Open the paper directly.</a>
              </p>
            </object>
          </section>

          <section id="citation">
            <h2>Citation</h2>
            <p>
              Nandhakumar, S. (2026). <em>The Frontline Exposure Gap: Evidence on AI Adoption in Retail and Service Occupations from Task-Level Usage Data</em>. Working paper.
            </p>

            <button class="copy-button" type="button" onclick="copyCitation()">Copy BibTeX</button>
            <pre id="bibtex">@misc{nandhakumar2026frontline,
  author       = {Sriramkrishnan Nandhakumar},
  title        = {The Frontline Exposure Gap: Evidence on AI Adoption in Retail and Service Occupations from Task-Level Usage Data},
  year         = {2026},
  month        = {July},
  note         = {Working paper},
  url          = {https://github.com/raamnandhakumar-eng/polecoai}
}</pre>
          </section>

          <section id="references">
            <h2>Selected references</h2>
            <ol class="references">
              <li>Acemoglu, Daron, and David Autor. 2011. “Skills, Tasks and Technologies: Implications for Employment and Earnings.” <em>Handbook of Labor Economics</em> 4B.</li>
              <li>Acemoglu, Daron, and Pascual Restrepo. 2019. “Automation and New Tasks: How Technology Displaces and Reinstates Labor.” <em>Journal of Economic Perspectives</em> 33(2).</li>
              <li>Brynjolfsson, Erik, Danielle Li, and Lindsey R. Raymond. 2025. “Generative AI at Work.” <em>Quarterly Journal of Economics</em> 140(2).</li>
              <li>Eloundou, Tyna, Sam Manning, Pamela Mishkin, and Daniel Rock. 2024. “GPTs Are GPTs: Labor Market Impact Potential of LLMs.” <em>Science</em> 384.</li>
              <li>Handa, Kunal, Alex Tamkin, Miles McCain, et al. 2025. “Which Economic Tasks Are Performed with AI? Evidence from Millions of Claude Conversations.” arXiv:2503.04761.</li>
              <li>Humlum, Anders, and Emilie Vestergaard. 2025. “The Unequal Adoption of ChatGPT Exacerbates Existing Inequalities among Workers.” <em>PNAS</em> 122(1).</li>
              <li>Massenkoff, Maxim, and Peter McCrory. 2026. “Labor Market Impacts of AI: A New Measure and Early Evidence.” Anthropic working paper.</li>
              <li>Shen, Judy Hanwen, and Alex Tamkin. 2026. “How AI Impacts Skill Formation.” arXiv:2601.20245.</li>
              <li>Yin, Michelle, and Burhan Ogut. 2026. “Who Uses AI? Platforms, Workforce, and AI Exposure.” arXiv:2605.21743.</li>
            </ol>
          </section>
        </article>

        <aside aria-label="Paper summary">
          <div class="box">
            <h2>Paper details</h2>
            <ul>
              <li><strong>Status:</strong> Working paper</li>
              <li><strong>Revision:</strong> July 2026</li>
              <li><strong>Author:</strong> Sriramkrishnan Nandhakumar</li>
              <li><strong>Data:</strong> Anthropic Economic Index, O*NET, BLS OEWS</li>
              <li><strong>Method:</strong> Descriptive task- and occupation-level analysis</li>
              <li><strong>Code:</strong> Open-source Python replication materials</li>
            </ul>
          </div>
        </aside>
      </div>

      <footer>
        Replication code, processed outputs, figures, tests, and documentation are maintained at
        <a href="https://github.com/raamnandhakumar-eng/polecoai" target="_blank" rel="noopener">github.com/raamnandhakumar-eng/polecoai</a>.
        Source datasets retain their original licenses. Inclusion of data sources does not imply endorsement of this analysis.
      </footer>
    </div>
  </main>

  <script>
    function copyCitation() {
      const text = document.getElementById('bibtex').innerText;
      navigator.clipboard.writeText(text).then(() => {
        const button = document.querySelector('.copy-button');
        const original = button.textContent;
        button.textContent = 'Copied';
        setTimeout(() => {
          button.textContent = original;
        }, 1600);
      }).catch(() => {
        alert('Copy failed. Select the BibTeX text manually.');
      });
    }
  </script>
</body>
</html>
