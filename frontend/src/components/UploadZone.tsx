import { ChangeEvent, useRef } from "react";
import { UploadCloud } from "lucide-react";

interface Props {
  onSelect(files: FileList): void;
  disabled?: boolean;
}

export function UploadZone({ onSelect, disabled }: Props) {
  const fileRef = useRef<HTMLInputElement | null>(null);

  const handleFiles = (event: ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files.length > 0) {
      onSelect(event.target.files);
      event.target.value = "";
    }
  };

  return (
    <div className="border border-dashed border-slate-700 rounded-3xl p-8 text-center bg-slate-900/40">
      <UploadCloud className="mx-auto mb-3 h-10 w-10 text-primary" />
      <p className="text-lg font-semibold mb-2">Upload PDFs</p>
      <p className="text-sm text-slate-400 mb-4">
        Drop multiple documents or browse your files. We will index them securely on-device.
      </p>
      <button
        className="px-6 py-2 rounded-full bg-primary hover:bg-primary/90 text-white disabled:opacity-50"
        onClick={() => fileRef.current?.click()}
        disabled={disabled}
      >
        {disabled ? "Processing..." : "Select files"}
      </button>
      <input
        ref={fileRef}
        type="file"
        accept="application/pdf"
        multiple
        hidden
        onChange={handleFiles}
      />
    </div>
  );
}
