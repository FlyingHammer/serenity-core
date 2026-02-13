export function TicketTable({ ticket }: { ticket: any }) {
  if (!ticket) return <p>No ticket for this signal.</p>
  const rows = [
    ['Lot Size', ticket.lot_size],
    ['Entry', `${ticket.order_type} @ ${ticket.entry_price}`],
    ['SL', `${ticket.stop_distance_pips} pips @ ${ticket.stop_price}`],
    ['TP1', `${ticket.take_profit_distance_pips} pips @ ${ticket.take_profit_price}`],
    ['Trailing activation', `${ticket.broker_fields?.activation_at_r}R / ${ticket.broker_fields?.trailing_activation_pips} pips`],
    ['Initial stop pips', ticket.broker_fields?.initial_stop_pips],
    ['Trailing step pips', ticket.broker_fields?.trailing_step_pips],
  ]
  return <table border={1} cellPadding={6}><tbody>{rows.map(([k,v])=><tr key={String(k)}><td>{k}</td><td>{String(v)}</td></tr>)}</tbody></table>
}
