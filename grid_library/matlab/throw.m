function throw( ExceptionInfo )
  disp(ExceptionInfo.tag)
  error( ExceptionInfo.message )
end

