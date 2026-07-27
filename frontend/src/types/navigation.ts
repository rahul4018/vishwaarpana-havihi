export type UserRole =
  | "admin"
  | "owner"
  | "priest"
  | "catering"
  | "customer";

export interface NavigationChild {
  id: string;
  title: string;
  description?: string;
  href: string;
  icon?: string;
  roles: UserRole[];
}

export interface NavigationSection {
  title: string;
  children: NavigationChild[];
}

export interface NavigationItem {
  id: string;
  title: string;
  href?: string;
  roles: UserRole[];
  sections?: NavigationSection[];
}