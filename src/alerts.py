"""Alert text in English and Hindi for the top risk cells. Template based, so it works offline
and never invents facts. Reasons come from the cell's own numbers."""
def reasons(r):
    out = []
    if r.get('dry_days', 0) >= 10: out.append(('no rain for %d days' % r['dry_days'], '%d दिन से बारिश नहीं' % r['dry_days']))
    if r.get('rh7', 100) < 40: out.append(('low humidity %d%%' % r['rh7'], 'कम नमी %d%%' % r['rh7']))
    if r.get('fires_past7', 0) > 0: out.append(('%d fire points nearby this week' % r['fires_past7'], 'इस हफ्ते पास में %d आग बिंदु' % r['fires_past7']))
    if r.get('T2M_MAX', 0) >= 30: out.append(('hot, %d C' % r['T2M_MAX'], 'तेज़ गर्मी, %d°C' % r['T2M_MAX']))
    if r.get('hist_rate', 0) >= 0.05: out.append(('fire-prone in past years', 'पिछले वर्षों में आग-प्रवण क्षेत्र'))
    if not out: out.append(('seasonal risk', 'मौसमी जोखिम'))
    return out[:3]

def level(p):
    return ('VERY HIGH', 'अति उच्च') if p >= 0.5 else ('HIGH', 'उच्च') if p >= 0.25 else ('MODERATE', 'मध्यम') if p >= 0.1 else ('LOW', 'निम्न')

def alert(r):
    en, hi = level(r['p']); rs = reasons(r)
    e = 'VAN AGNI %s fire risk (%d%%) near %.2fN %.2fE, next 7 days. Why: %s. Advisory only: verify with beat staff.' % (en, r['p']*100, r['lat'], r['lon'], '; '.join(x[0] for x in rs))
    h = 'वन अग्नि: %.2fN %.2fE के पास अगले 7 दिन %s आग जोखिम (%d%%). कारण: %s. केवल सलाह: बीट स्टाफ से पुष्टि करें.' % (r['lat'], r['lon'], hi, r['p']*100, '; '.join(x[1] for x in rs))
    return e, h
