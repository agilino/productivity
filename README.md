# productivity

In this repository you can find tools, that help us code and manage our work better.

## Github KPI tool

While Key Performance Indicators (KPIs) are old school they give insights to the team managers,
if individual developers are shy to comment, review or contribute or delete code of their colleagues.
Together with Objectives and Key Results (OKRs) it can provide a holistic view of teams productivity.

To use this tool make sure to have [github cli installed](https://github.com/cli/cli#installation) and run:

```bash
python gh_stats.py repo/project excluded-user 2023-08-01 2023-08-31
```

This tool of course does not account for the contributions that have been done in pair-programming and it also not account for the reviews that have been done directly without using github. It is always good to meet and provide feedback in person or in a call, it makes also sense to write a summary of the comments or change requests afterwards inside of the github PR.
