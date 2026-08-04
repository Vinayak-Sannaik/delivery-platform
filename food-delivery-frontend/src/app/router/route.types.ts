// Define the object as a const to preserve literal types
export const UserRole = {
  CUSTOMER: "CUSTOMER",
  RESTAURANT_OWNER: "RESTAURANT_OWNER",
  DELIVERY_PARTNER: "DELIVERY_PARTNER",
  ADMIN: "ADMIN",
} as const;

// Define the type alias for type checking
export type UserRole = (typeof UserRole)[keyof typeof UserRole];