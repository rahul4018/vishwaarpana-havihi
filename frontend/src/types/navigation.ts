/**
 * User roles supported by the application.
 */
export type UserRole =
  | "admin"
  | "owner"
  | "priest"
  | "catering"
  | "customer";

/**
 * Child item displayed inside a Mega Menu section.
 */
export interface NavigationChild {
  id: string;

  title: string;

  description: string;

  href: string;

  /**
   * Lucide icon name.
   * Example:
   * LayoutDashboard
   * Building2
   * CalendarDays
   */
  icon: string;

  roles: UserRole[];

  badge?: string;

  disabled?: boolean;

  external?: boolean;
}

/**
 * A column inside the Mega Menu.
 */
export interface NavigationSection {
  title: string;

  children: NavigationChild[];
}

/**
 * Top-level navigation item.
 */
export interface NavigationItem {
  id: string;

  title: string;

  /**
   * Lucide icon name.
   */
  icon?: string;

  /**
   * Used when this menu directly navigates to a page.
   * Example:
   * Dashboard
   */
  href?: string;

  /**
   * Used for Mega Menu.
   */
  sections?: NavigationSection[];

  /**
   * Roles allowed to view this menu.
   */
  roles: UserRole[];

  badge?: string;

  disabled?: boolean;
}