#!/usr/bin/env python3
"""
Calculate tier 2 (4-digit) activity summary for full-time workers.
Short, readable version for verification.
"""

import pandas as pd

# Tier 1 category names (2-digit codes)
TIER1_NAMES = {
    "01": "Personal Care",
    "02": "Household Activities",
    "03": "Caring For & Helping HH Members",
    "04": "Caring For & Helping NonHH Members",
    "05": "Work & Work-Related Activities",
    "06": "Education",
    "07": "Consumer Purchases",
    "08": "Professional & Personal Care Services",
    "09": "Household Services",
    "10": "Government Services & Civic Obligations",
    "11": "Eating and Drinking",
    "12": "Socializing, Relaxing, and Leisure",
    "13": "Sports, Exercise, and Recreation",
    "14": "Religious and Spiritual Activities",
    "15": "Volunteer Activities",
    "16": "Telephone Calls",
    "18": "Traveling",
    "50": "Data Codes",
}

# Tier 2 category names (4-digit codes) from ATUS Activity Lexicon 2024
TIER2_NAMES = {
    # 01 - Personal Care
    "0101": "Sleeping",
    "0102": "Grooming",
    "0103": "Health-related Self Care",
    "0104": "Personal Activities",
    "0105": "Personal Care Emergencies",
    "0199": "Personal Care, n.e.c.",
    # 02 - Household Activities
    "0201": "Housework",
    "0202": "Food & Drink Prep., Presentation, & Clean-up",
    "0203": "Interior Maintenance, Repair, & Decoration",
    "0204": "Exterior Maintenance, Repair, & Decoration",
    "0205": "Lawn, Garden, and Houseplants",
    "0206": "Animals and Pets",
    "0207": "Vehicles",
    "0208": "Appliances, Tools, and Toys",
    "0209": "Household Management",
    "0299": "Household Activities, n.e.c.",
    # 03 - Caring For & Helping Household Members
    "0301": "Caring For & Helping HH Children",
    "0302": "Activities Related to HH Children's Education",
    "0303": "Activities Related to HH Children's Health",
    "0304": "Caring For Household Adults",
    "0305": "Helping Household Adults",
    "0399": "Caring For & Helping HH Members, n.e.c.",
    # 04 - Caring For & Helping NonHH Members
    "0401": "Caring For & Helping NonHH Children",
    "0402": "Activities Related to Nonhh Children's Education",
    "0403": "Activities Related to Nonhh Children's Health",
    "0404": "Caring For Nonhousehold Adults",
    "0405": "Helping Nonhousehold Adults",
    "0499": "Caring For & Helping NonHH Members, n.e.c.",
    # 05 - Work & Work-Related Activities
    "0501": "Working",
    "0502": "Work-Related Activities",
    "0503": "Other Income-generating Activities",
    "0504": "Job Search and Interviewing",
    "0599": "Work and Work-Related Activities, n.e.c.",
    # 06 - Education
    "0601": "Taking Class",
    "0602": "Extracurricular School Activities (Except Sports)",
    "0603": "Research/Homework",
    "0604": "Registration/Administrative activities",
    "0699": "Education, n.e.c.",
    # 07 - Consumer Purchases
    "0701": "Shopping (Store, Telephone, Internet)",
    "0702": "Researching Purchases",
    "0703": "Security Procedures Rel. to Consumer Purchases",
    "0799": "Consumer Purchases, n.e.c.",
    # 08 - Professional & Personal Care Services
    "0801": "Childcare Services",
    "0802": "Financial Services and Banking",
    "0803": "Legal Services",
    "0804": "Medical and Care Services",
    "0805": "Personal Care Services",
    "0806": "Real Estate",
    "0807": "Veterinary Services",
    "0808": "Security Procedures Rel. to Professional/Personal Svcs.",
    "0899": "Professional and Personal Services, n.e.c.",
    # 09 - Household Services
    "0901": "Household Services (not done by self)",
    "0902": "Home Maint/Repair/Decor/Construction (not done by self)",
    "0903": "Pet Services (not done by self, not vet)",
    "0904": "Lawn & Garden Services (not done by self)",
    "0905": "Vehicle Maint. & Repair Services (not done by self)",
    "0999": "Household Services, n.e.c.",
    # 10 - Government Services & Civic Obligations
    "1001": "Using Government Services",
    "1002": "Civic Obligations & Participation",
    "1003": "Waiting Associated w/Govt Svcs or Civic Obligations",
    "1004": "Security Procedures Rel. to Govt Svcs/Civic Obligations",
    "1099": "Government Services, n.e.c.",
    # 11 - Eating and Drinking
    "1101": "Eating and Drinking",
    "1102": "Waiting associated with eating & drinking",
    "1199": "Eating and Drinking, n.e.c.",
    # 12 - Socializing, Relaxing, and Leisure
    "1201": "Socializing and Communicating",
    "1202": "Attending or Hosting Social Events",
    "1203": "Relaxing and Leisure",
    "1204": "Arts and Entertainment (other than sports)",
    "1205": "Waiting Associated with Socializing, Relaxing, and Leisure",
    "1299": "Socializing, Relaxing, and Leisure, n.e.c.",
    # 13 - Sports, Exercise, and Recreation
    "1301": "Participating in Sports, Exercise, or Recreation",
    "1302": "Attending Sporting/Recreational Events",
    "1303": "Waiting Associated with Sports, Exercise, & Recreation",
    "1304": "Security Procedures Rel. to Sports, Exercise, & Recreation",
    "1399": "Sports, Exercise, & Recreation, n.e.c.",
    # 14 - Religious and Spiritual Activities
    "1401": "Religious/Spiritual Practices",
    "1499": "Religious and Spiritual Activities, n.e.c.",
    # 15 - Volunteer Activities
    "1501": "Administrative & Support Activities",
    "1502": "Social Service & Care Activities (Except Medical)",
    "1503": "Indoor & Outdoor Maintenance, Building, & Clean-up Activities",
    "1504": "Participating in Performance & Cultural Activities",
    "1505": "Attending Meetings, Conferences, & Training",
    "1506": "Public Health & Safety Activities",
    "1507": "Waiting Associated with Volunteer Activities",
    "1508": "Security procedures related to volunteer activities",
    "1599": "Volunteer Activities, n.e.c.",
    # 16 - Telephone Calls
    "1601": "Telephone Calls (to or from)",
    "1602": "Waiting Associated with Telephone Calls",
    "1699": "Telephone Calls, n.e.c.",
    # 18 - Traveling
    "1801": "Travel Related to Personal Care",
    "1802": "Travel Related to Household Activities",
    "1803": "Travel Related to Caring For & Helping HH Members",
    "1804": "Travel Related to Caring For & Helping Nonhh Members",
    "1805": "Travel Related to Work",
    "1806": "Travel Related to Education",
    "1807": "Travel Related to Consumer Purchases",
    "1808": "Travel Related to Using Professional and Personal Care Services",
    "1809": "Travel Related to Using Household Services",
    "1810": "Travel Related to Using Govt Services & Civic Obligations",
    "1811": "Travel Related to Eating and Drinking",
    "1812": "Travel Related to Socializing, Relaxing, and Leisure",
    "1813": "Travel Related to Sports, Exercise, & Recreation",
    "1814": "Travel Related to Religious/Spiritual Activities",
    "1815": "Travel Related to Volunteer Activities",
    "1816": "Travel Related to Telephone Calls",
    "1818": "Security Procedures Related to Traveling",
    "1899": "Traveling, n.e.c.",
    # 50 - Data Codes
    "5001": "Unable to Code",
    "5099": "Data codes, n.e.c.",
}

# Load data
df = pd.read_csv("atussum-2024/atussum_2024.dat")
print(f"Loaded {len(df):,} respondents")

# Filter: full-time workers (employed + full-time)
df = df[(df['TELFS'].isin([1, 2])) & (df['TRDPFTPT'] == 1)].copy()
print(f"Full-time workers: {len(df):,}")

# Identify activity columns (t followed by 6 digits)
activity_cols = [c for c in df.columns if c.startswith('t') and c[1:].isdigit()]
print(f"Activity columns: {len(activity_cols)}")

# Create day type indicator (Mon-Fri = weekday)
df['is_weekday'] = df['TUDIARYDAY'].isin([2, 3, 4, 5, 6])

# Get unique 4-digit codes from activity columns
tier2_codes = sorted(set(col[1:5] for col in activity_cols))
print(f"Tier 2 categories: {len(tier2_codes)}")

# Aggregate each person's activities to tier 2 level
for code in tier2_codes:
    cols = [c for c in activity_cols if c[1:5] == code]
    df[f't2_{code}'] = df[cols].sum(axis=1)

# Calculate weighted averages for each day type
def weighted_avg(data, value_col, weight_col='TUFINLWGT'):
    return (data[value_col] * data[weight_col]).sum() / data[weight_col].sum()

results = []
for code in tier2_codes:
    col = f't2_{code}'

    weekday_avg = weighted_avg(df[df['is_weekday']], col)
    weekend_avg = weighted_avg(df[~df['is_weekday']], col)
    week_avg = (5/7) * weekday_avg + (2/7) * weekend_avg

    results.append({
        'tier2_code': code,
        'tier2_name': TIER2_NAMES.get(code, "Unknown"),
        'tier1_code': code[:2],
        'tier1_name': TIER1_NAMES.get(code[:2], "Unknown"),
        'weekday_hrs': weekday_avg / 60,
        'weekend_hrs': weekend_avg / 60,
        'week_avg_hrs': week_avg / 60,
    })

# Create summary dataframe
summary = pd.DataFrame(results)

# Verify totals add to 24 hours
print(f"\nTotal hours (weekday): {summary['weekday_hrs'].sum():.2f}")
print(f"Total hours (weekend): {summary['weekend_hrs'].sum():.2f}")
print(f"Total hours (week avg): {summary['week_avg_hrs'].sum():.2f}")

# Save
summary.to_csv("atus_tier2_summary_simple.csv", index=False)
print(f"\nSaved to atus_tier2_summary_simple.csv")

# Show top categories by time spent
print("\nTop 10 tier 2 categories (week average hours):")
top10 = summary.nlargest(10, 'week_avg_hrs')
for _, row in top10.iterrows():
    print(f"  {row['tier2_code']} {row['tier2_name']}: {row['week_avg_hrs']:.2f} hrs")
