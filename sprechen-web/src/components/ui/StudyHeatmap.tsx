import { useEffect, useMemo, useRef, useState } from "react";
import type { HeatmapCell } from "@/types";

interface Props {
  cells: HeatmapCell[];
}

const LEVEL_BG: Record<HeatmapCell["level"], string> = {
  0: "bg-gray-100",
  1: "bg-green-200",
  2: "bg-green-400",
  3: "bg-green-600",
  4: "bg-green-800",
};

const MONTH_LABELS = [
  "Jan",
  "Feb",
  "Mär",
  "Apr",
  "Mai",
  "Jun",
  "Jul",
  "Aug",
  "Sep",
  "Okt",
  "Nov",
  "Dez",
];

interface Column {
  cells: (HeatmapCell | null)[];
  monthLabel: string | null;
}

export function StudyHeatmap({ cells }: Props) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const [hover, setHover] = useState<HeatmapCell | null>(null);

  const columns: Column[] = useMemo(() => {
    if (cells.length === 0) return [];
    const byDate = new Map(cells.map((c) => [c.date, c]));
    const first = new Date(cells[0].date);
    const last = new Date(cells[cells.length - 1].date);

    // Start at the Monday of the week containing `first`
    const start = new Date(first);
    const dayIdx = (start.getDay() + 6) % 7; // 0 = Monday
    start.setDate(start.getDate() - dayIdx);

    const cols: Column[] = [];
    const cursor = new Date(start);
    let lastMonth = -1;
    while (cursor <= last) {
      const colCells: (HeatmapCell | null)[] = [];
      let monthLabel: string | null = null;
      for (let row = 0; row < 7; row++) {
        const iso = cursor.toISOString().slice(0, 10);
        const cell = byDate.get(iso) ?? null;
        colCells.push(cell);
        if (cell && cursor.getDate() <= 7 && cursor.getMonth() !== lastMonth) {
          monthLabel = MONTH_LABELS[cursor.getMonth()];
          lastMonth = cursor.getMonth();
        }
        cursor.setDate(cursor.getDate() + 1);
      }
      cols.push({ cells: colCells, monthLabel });
    }
    return cols;
  }, [cells]);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollLeft = scrollRef.current.scrollWidth;
    }
  }, [columns.length]);

  if (cells.length === 0) {
    return (
      <p className="py-6 text-center text-sm text-gray-400">
        Noch keine Aktivität.
      </p>
    );
  }

  return (
    <div className="relative">
      <div ref={scrollRef} className="overflow-x-auto">
        <div className="inline-flex flex-col gap-1 pb-2">
          {/* month labels */}
          <div className="flex gap-[3px] pl-6">
            {columns.map((col, i) => (
              <div
                key={i}
                className="h-3 w-[10px] text-[9px] font-medium text-gray-500"
              >
                {col.monthLabel ?? ""}
              </div>
            ))}
          </div>
          <div className="flex gap-[3px]">
            {/* weekday labels */}
            <div className="flex w-5 flex-col justify-between text-[9px] text-gray-400">
              <span>Mo</span>
              <span>Mi</span>
              <span>Fr</span>
            </div>
            {/* grid */}
            {columns.map((col, ci) => (
              <div key={ci} className="flex flex-col gap-[3px]">
                {col.cells.map((cell, ri) => (
                  <div
                    key={ri}
                    onMouseEnter={() => cell && setHover(cell)}
                    onMouseLeave={() => setHover(null)}
                    className={`h-[10px] w-[10px] rounded-sm ${
                      cell ? LEVEL_BG[cell.level] : "bg-transparent"
                    }`}
                    title={
                      cell
                        ? `${cell.date}: ${cell.count} Aktivitäten`
                        : undefined
                    }
                  />
                ))}
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="mt-2 flex items-center justify-end gap-2 text-[10px] text-gray-500">
        <span>Weniger</span>
        {([0, 1, 2, 3, 4] as const).map((lvl) => (
          <div
            key={lvl}
            className={`h-2.5 w-2.5 rounded-sm ${LEVEL_BG[lvl]}`}
          />
        ))}
        <span>Mehr</span>
      </div>

      {hover && (
        <div className="mt-2 text-xs text-gray-600">
          {hover.date}: {hover.count} Aktivitäten
        </div>
      )}
    </div>
  );
}
