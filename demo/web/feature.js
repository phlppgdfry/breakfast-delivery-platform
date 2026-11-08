export function inspect(r) {
  const next = {
    confirmed: "Start preparation",
    preparing: "Hand to delivery partner",
    out_for_delivery: "Confirm delivery",
  };
  return {
    fields: [
      ["Breakfast", `${r.quantity} × ${r.box}`],
      ["Delivery date", r.delivery],
      ["Postal code", r.postal],
      ["Reservation total", r.value],
      ["Allergens acknowledged", r.allergens_ack ? "Yes" : "No"],
    ],
    forms: [
      ...(next[r.state]
        ? [
            {
              title: "Fulfilment",
              action: "advance",
              button: next[r.state],
              fields: [],
            },
          ]
        : []),
      {
        title: "Reserve breakfast",
        help: "Classic: wheat, milk, egg. Brunch: wheat, milk, egg, sesame. Availability is checked when you reserve. Demo clock: 20:00, before the 22:00 cutoff.",
        action: "create",
        button: "Reserve breakfast box",
        success:
          "Reservation confirmed. Your order is selected and delivery capacity has been updated. No payment was collected.",
        fields: [
          {
            key: "customer",
            label: "Customer name · fictional only",
            maxLength: 60,
          },
          {
            key: "box",
            label: "Breakfast box",
            options: [
              { value: "Classic", label: "Classic · €12.50" },
              { value: "Brunch", label: "Brunch · €18.00" },
            ],
          },
          {
            key: "quantity",
            label: "Number of boxes",
            type: "number",
            min: 1,
            max: 4,
            value: 1,
          },
          { key: "postal", label: "Postal code", options: ["9000", "9030"] },
          {
            key: "slot",
            label: "Delivery window · tomorrow",
            options: ["06:00–07:00", "07:00–08:00"],
          },
          {
            key: "allergens_ack",
            label: "I have reviewed the allergens listed above",
            type: "checkbox",
          },
        ],
      },
    ],
    note: "This is a reservation simulation. Payments, food safety operations, routing and live tracking are outside this demo.",
  };
}
