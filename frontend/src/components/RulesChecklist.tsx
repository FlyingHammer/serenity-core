export function RulesChecklist({ checklist, values }: { checklist: Record<string, boolean>; values: Record<string, any> }) {
  return <table border={1} cellPadding={6}><thead><tr><th>Rule</th><th>Pass</th><th>Value</th></tr></thead><tbody>
    {Object.keys(checklist).map((k) => <tr key={k}><td>{k}</td><td>{checklist[k] ? '✅' : '❌'}</td><td>{String(values[k] ?? '-')}</td></tr>)}
  </tbody></table>
}
