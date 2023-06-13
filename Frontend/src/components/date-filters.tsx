import { useRadioGroup, HStack } from "@chakra-ui/react"
import RadioButtons from "./radio-buttons"

type DateFilterProps ={
    onChange:(selectedDate:any)=>void
}

const dateMap = {
    'Last 7 days':1,
    'Last 30 days':2,
    'Last 6 month':7,
    'All Time':'all'
}

// Step 2: Use the `useRadioGroup` hook to control a group of custom radios.
function DateFilters(props:DateFilterProps) {
    const options = ['Last 7 days', 'Last 30 days', 'Last 6 month','All Time']
  
    const { getRootProps, getRadioProps } = useRadioGroup({
      name: 'date',
      defaultValue: 'All Time',
    // @ts-ignore
      onChange:(dateSelected)=>props.onChange(dateMap[dateSelected] )
        
    })
  
    const group = getRootProps()
  
    return (
      <HStack {...group}>
        {options.map((value) => {
          const radio = getRadioProps({ value })
          return (
            <RadioButtons  key={value} {...radio}>
              {value}
            </RadioButtons>
          )
        })}
      </HStack>
    )
  }

  export default DateFilters