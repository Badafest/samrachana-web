import AnalysisTable from "../AnalysisTable";
import Icon from "../Elements/Icon";
import ViewTopBar from "../Elements/ViewTopBar";

export default function TableView() {
  return (
    <>
      <ViewTopBar>
        <Icon className="" onClick={() => {}}>
          H
        </Icon>
      </ViewTopBar>
      <AnalysisTable />
    </>
  );
}
