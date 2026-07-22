# A Third of American Workers Are Missing From the AI Boom — I Went Looking For Them in the Data

*Draft blog post (~900 words). NOTE TO AUTHOR: the bracketed spots need your
real experience, same as the paper. Personalize the voice throughout —
this draft is scaffolding, not a finished post under your name.*

I used to work retail. [ONE SENTENCE: where, roughly when, doing what.]
Lately I've been doing empirical work on how AI is entering the economy, and
I kept noticing that the charts in AI-adoption studies never seemed to
include anyone I'd worked a shift with. So I pulled the public data from the
Anthropic Economic Index — millions of real AI conversations mapped to
official occupational task categories — joined it to government employment
data, and measured it properly. The full paper and code are here: [links].

Here's what I found.

**Frontline service jobs — retail, admin support, food service, personal
care — hold 31.7% of US employment and 11.1% of real-world AI usage.**
Software and math occupations are the mirror image: 3.4% of jobs, 37% of
usage. Relative to its size in the labor market, retail sales work shows up
in AI usage data at about one-fortieth the rate of software work. Food
service, at one one-hundred-eightieth.

Three things about that gap surprised me more than the gap itself.

**First, it's bigger than the official numbers say.** The frontline category
that looked most AI-engaged — office and administrative support — turns out
to be stuffed with occupations that aren't really frontline at all.
"Bioinformatics Technicians" and "Computer Operators" are filed under
administrative support in the government's occupation codes, and they drag
the average up. Strip them out and the admin-support number nearly halves.
The workers standing at registers and answering phones are even further from
the AI economy than the raw statistics suggest.

**Second, it isn't closing.** Comparing snapshots from early and late 2025,
every occupation group's AI usage grew roughly in place. Nothing converged.
Food service actually slipped. Six months of the fastest technology adoption
in memory, and the map of who uses AI barely moved — usage got deeper where
it was already deep.

**Third — and this is the one that changed how I think about it — when AI
does reach frontline work, it shows up as automation, not as a tool.** The
data classifies each conversation by interaction style: delegation
("write this for me") versus collaboration ("help me understand this").
Frontline administrative tasks show *more* delegation-style usage (63%) than
software tasks do (58%). Software engineers use AI to learn and iterate on
their own work. When frontline tasks meet AI, the task is simply handed
over. And there's now experimental evidence from Anthropic's own researchers
that the delegation style is precisely the one that builds no skills in the
person using it. So the workers getting the least AI exposure are also
getting the least value per unit of the exposure they get.

By early 2026, the newest data shows where this is heading. It's not
"frontline versus professional" anymore. It's a split *inside* frontline
work: Customer Service Representatives — phone, chat, email work — now rank
among the most AI-exposed occupations in the entire economy, right next to
computer programmers. Meanwhile 39% of frontline occupations, including
every category of cook, register literally zero observed exposure. The
dividing line is whether your work happens through a screen or in a room
with another person.

Why does the gap exist? The data alone can't say, but having done the work
helps. Part of it is obvious: no chatbot stocks a shelf or de-escalates an
angry customer at closing time. But frontline jobs are full of information
work too — scheduling, customer correspondence, reports — and the data shows
exactly those tasks *can* be done with AI, just at tiny volume.

[YOUR PARAGRAPH GOES HERE: the access story from your own shifts. Could you
have used an AI tool at work if you'd wanted to? What device, what downtime,
what policy? And at your startup — what did you automate first, and what
stopped you elsewhere? 4-6 sentences, concrete.]

That's the part I find genuinely worth worrying about. The one rigorous
experiment showing big AI gains for frontline-adjacent workers — customer
support agents, in a study by Brynjolfsson, Li, and Raymond — involved an
employer deliberately *giving* workers an AI assistant built to help them,
not replace their judgment. The gap I measured isn't physics. It's a
default: of product design, of workplace policy, of who technology gets
built for first. Defaults can be changed.

A third of the workforce is currently participating in the AI economy mainly
as its object — the thing being scheduled, scripted, and eventually
automated — rather than as users. Whether that stays true seems to me one of
the most consequential open questions about this technology, and it's
answerable with data that's sitting in public repositories right now.

The full analysis — five findings, robustness checks, all code and data — is
in this repository, together with the working paper. If you work
frontline or run a small business and your experience with AI contradicts
anything here, I genuinely want to hear it: [contact].
