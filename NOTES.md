# What I checked, and what the agent got wrong

## What the agent got wrong

The main problem I caught was the wear calculation. It used integer division, so a partial service interval was rounded down instead of giving the real percentage. For example, 12,000 km out of a 15,000 km interval should be 80%, but the old calculation could return 0%. I changed the division from `//` to `/`.

I also learned not to accept an AI agent's changes just because the code looks cleaner. I checked the actual behavior and the edge cases instead.

## What I checked before I accepted its work

I checked that the service interval is still 15,000 km and the warning threshold is still 80%. I also checked the boundary around the warning point: 12,000 km should be 80% and should be flagged, while a value just below 80% should not be flagged.

Before accepting the final work, I ran `python verify.py` and made sure all 11 checks passed.

## What the data actually said

I compared the cars that later broke down with the cars that did not instead of assuming that the obvious factors were important. The useful signals came from factors such as kilometres since service, daily use, and load. Total mileage looked like an obvious predictor at first, but it did not clearly separate the breakdown and non-breakdown groups.

This showed me why checking the data is more reliable than making an assumption based only on a car's total mileage or age.
