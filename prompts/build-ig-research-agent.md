# Build an Instagram Research Agent

Paste this into Claude Code. It walks you through building an agent that finds the reels breaking out in your niche and turns them into hooks and filmable ideas, step by step.

Full guide: [ezjonline.com/resources/ig-research-agent](https://www.ezjonline.com/resources/ig-research-agent). Or start from the n8n template: [IG_Research_Agent_Demo.json](../n8n%20templates/IG_Research_Agent_Demo.json).

```
Help me build an Instagram Research Agent for my niche, step by step. Ask me one question at a time and wait for my answer.

1. Ask for my Instagram handle and 10 to 15 competitor accounts that post often in my niche.
2. Help me create an Apify account and API token, and test the Instagram reel scraper on one account.
3. Design an Airtable base with tables: Competitors, My Reels, Outliers, Reports, and Served History (a memory of every idea already sent, so nothing repeats for 28 days).
4. Write the analysis prompt: an outlier is a reel with far more views than that account's median. For each outlier, explain the hook, format and topic, then write 20 hooks and 5 to 7 filmable ideas in my voice.
5. Build an n8n workflow that runs weekly: scrape competitors and my reels, store them, find outliers, skip anything in Served History, run the analysis, save the report, and post it to Slack.
6. Test it end to end with one run and show me the report.

Never hardcode API keys in the workflow. Use n8n credentials.
```

Want it built for you? [Book a free AI Audit](https://www.ezjonline.com/ai-audit?utm_source=github&utm_medium=prompts&utm_campaign=ig-research-agent).
