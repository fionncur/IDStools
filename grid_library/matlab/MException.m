function out = MException( arg1, arg2, arg3, arg4, arg5 )

  if nargin < 2
    error( sprintf( 'MException:missing_arguments: MException requires at least 2 input arguments; only %d arguments recieved', nargin ) )
  end

  out.tag = arg1;
  if nargin == 2
    out.message = arg2;
  elseif nargin == 3
    out.message = sprintf( arg2 , arg3 );
  elseif nargin == 4
    out.message = sprintf( arg2 , arg3 , arg4 );
  elseif nargin == 5
    out.message = sprintf( arg2 , arg3 , arg5 );
  end

end
