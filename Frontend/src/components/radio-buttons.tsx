import { useRadio ,Box} from "@chakra-ui/react";


// 1. Create a component that consumes the `useRadio` hook
function RadioButtons (props:any) {
    const { getInputProps, getRadioProps } = useRadio(props)
  
    const input = getInputProps()
    const checkbox = getRadioProps()
  
    return (
      <Box as='label'>
        <input {...input} />
        <Box
          {...checkbox}
          cursor='pointer'
          borderWidth='1px'
          borderRadius='md'
          fontSize={"xs"}
          boxShadow='sm'
          _checked={{
            bg: 'telegram.600',
            color: 'white',
            borderColor: 'telegram.600',
          }}
          _focus={{
            boxShadow: 'outline',
          }}
          px={3}
          py={2}
        >
          {props.children}
        </Box>
      </Box>
    )
  }

  export default RadioButtons;