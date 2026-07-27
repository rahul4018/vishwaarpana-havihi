import Cookies from "js-cookie";
import { STORAGE_KEYS } from "@/constants/storage";

export const cookieStorage = {
  getAccessToken() {
    return Cookies.get(STORAGE_KEYS.ACCESS_TOKEN);
  },

  setAccessToken(token: string) {
    Cookies.set(STORAGE_KEYS.ACCESS_TOKEN, token, {
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
    });
  },

  removeAccessToken() {
    Cookies.remove(STORAGE_KEYS.ACCESS_TOKEN);
  },

  getRefreshToken() {
    return Cookies.get(STORAGE_KEYS.REFRESH_TOKEN);
  },

  setRefreshToken(token: string) {
    Cookies.set(STORAGE_KEYS.REFRESH_TOKEN, token, {
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
    });
  },

  removeRefreshToken() {
    Cookies.remove(STORAGE_KEYS.REFRESH_TOKEN);
  },

  clear() {
    this.removeAccessToken();
    this.removeRefreshToken();
  },
};