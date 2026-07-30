Order Created
      │
      ▼
Order Service
      │
      ▼
Outbox (orders)
      │
      ▼
Kafka
      │
      ▼
Delivery Consumer
      │
      ▼
Create Delivery (PENDING)
      │
      ▼
Persist Delivery
      │
      ▼
AssignmentService
      │
      ├── Find available partner
      ├── Assign partner
      ├── Mark unavailable
      ├── Create DeliveryAssigned event
      ▼
Outbox (delivery)
      │
      ▼
Kafka (delivery-events)
      │
      ▼
Order Service Consumer
      │
      ▼
Order → READY