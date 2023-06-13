import { Alert, AlertDescription, AlertIcon, Box, Spinner } from "@chakra-ui/react";
import { Chart, GoogleChartWrapperChartType, GoogleChartOptions, ChartWrapperOptions } from "react-google-charts";


type PieChartProps = {
  type:GoogleChartWrapperChartType | undefined
  options:{
    title:string
  },
  data?:(string | number)[][] 
}

const Loader = function(){
  return <span>Loading...</span>
}

const PieChart = function(props:GoogleChartOptions) {

  if(!props.data){
    return <Box  height={"400px"}>
      <Spinner/>
    </Box>
  }

  console.log(props.data)
  if(!props.data[1]){
    return <Alert status="warning">
        <AlertIcon/>
        <AlertDescription maxWidth={300}>
        No data was recived from DB
        Please make sure you are connecet to the right group/user          
        </AlertDescription>
      </Alert>
  }

  return  <Chart
  chartType={props.type}
  data={props.data}
  loader={<Loader/>}
  options={props.options}
  width={"100%"}
  height={"400px"}
/>
 
}

export default PieChart
