import Icon from "../Elements/Icon";
import MemberTree from "../MemberTree";
import ViewTopBar from "../Elements/ViewTopBar";

export default function TreeView() {
  return (
    <>
      <ViewTopBar>
        <Icon className="" onClick={() => {}}>
          T
        </Icon>
      </ViewTopBar>
      <MemberTree />
    </>
  );
}
