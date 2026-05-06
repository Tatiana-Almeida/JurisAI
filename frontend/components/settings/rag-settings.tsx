import type { RAGSettings as RAGSettingsType } from "@/types/knowledge-base";
import { RAGSettingsPanel } from "@/components/knowledge-base/rag-settings-panel";

type RAGSettingsProps = {
  settings?: RAGSettingsType;
};

export function RAGSettings({ settings }: RAGSettingsProps) {
  return <RAGSettingsPanel settings={settings} />;
}
