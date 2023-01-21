import { ILoad, ISegment, ISupport } from "../../slices/structure.slice";
import { useAppSelector } from "../../store";
import LoadForm from "./LoadForm";
import SegmentForm from "./SegmentForm";
import SupportForm from "./SupportForm";

import { useState, useEffect } from "react";

export default function EditDeleteForm() {
  const { selected } = useAppSelector((state) => state.app.data);
  const [member, setMember] = useState<ISegment | ISupport | ILoad>();
  const { segments, loads, supports } = useAppSelector(
    (state) => state.structure.members
  );
  useEffect(() => {
    setMember(
      [...segments, ...loads, ...supports].find(
        (member) => member.name === selected
      )
    );
  }, [selected]);

  return (
    <div className="bg-primary_light text-contrast1 rounded p-2">
      {member ? (
        member.class === "segment" ? (
          <SegmentForm edit={member} />
        ) : member.class === "support" ? (
          <SupportForm edit={member} />
        ) : (
          <LoadForm edit={member} />
        )
      ) : (
        "No member selected"
      )}
    </div>
  );
}
