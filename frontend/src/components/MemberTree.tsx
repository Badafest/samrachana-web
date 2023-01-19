import { useState, useRef, useEffect } from "react";

export default function MemberTree() {
  const [width, setWidth] = useState<number>(0);
  const [height, setHeight] = useState<number>(0);

  const tableRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = tableRef.current?.parentElement;
    if (container) {
      const rect = container.getBoundingClientRect();
      setWidth(rect.width);
      setHeight(rect.height);
    }
  }, []);

  return (
    <div
      ref={tableRef}
      className="absolute bg-secondary"
      style={{ width, height }}
    ></div>
  );
}
