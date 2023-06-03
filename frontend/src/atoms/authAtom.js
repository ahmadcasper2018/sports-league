import { atom } from "recoil";

export const tokenState = atom({
  key: "tokenState",
  default: "", // Initial value is an empty string
});
