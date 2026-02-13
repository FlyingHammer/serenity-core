export function SimResultsCard({ sim }: { sim: any }) {
  if (!sim) return null
  return <div style={{border:'1px solid #ddd', padding:10}}>
    <h4>Quick Sim Results</h4>
    <p>Trades: {sim.trades} | Win rate: {sim.win_rate}% | Avg R: {sim.avg_r}</p>
    <p>Expectancy: {sim.expectancy} | PF: {sim.profit_factor} | Max DD: {sim.max_drawdown_r}R</p>
    {sim.sample_warning && <p style={{color:'orange'}}>{sim.sample_warning}</p>}
  </div>
}
