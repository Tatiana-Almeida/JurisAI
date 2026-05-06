import type { OCRSettings as OCRSettingsType } from "@/types/ocr";
import { OCRSettingsPanel } from "@/components/ocr/ocr-settings-panel";

type OCRSettingsProps = {
  settings?: OCRSettingsType;
};

export function OCRSettings({ settings }: OCRSettingsProps) {
  return <OCRSettingsPanel settings={settings} />;
}
