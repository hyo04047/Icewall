# Hard Programming

각 코드를 보고 어느 부분이 Secure하지 않은지 고르고 이유를 작성한 후, 수정하세요.

작성한 답안은 icewall.executive@gmail.com으로 보내주면 됩니다.

... 은 생략된 코드이므로 신경쓰지 마세요. 주어진 코드 내에서만 고르면 됩니다.



1. ```java
   <%@page language=”java” pageEncoding=”UTF-8”%><%@page import=”java.io.*”%>
   <%
    String fileName = request.getParameter(“P”);

    if (fileName==null || “”.equals(fileName)) fileName = “dummy.txt”;
    BufferedInputStream bis = null;
    BufferedOutputStream bos = null;
    FileInputStream fis = null;

    try {
   	fileName = fileName.replaceAll(“\n”, “”).replaceAll(“\r”, “”);
   	response.setHeader(“Content-Disposition”, 	
                          				“attachment;filename=”+fileName+”;”);
   	......

    	byte[] buffer = new byte[1024];
    	fis = new FileInputStream(“C:/datas/” + fileName);
    	bis = new BufferedInputStream(fis);
    	bos = new BufferedOutputStream(response.getOutputStream());
    
    	int read;
    	while((read = bis.read(buffer, 0, 1024)) != -1) {
   		 bos.write(buffer,0,read);
    	}
    }  catch(Exception e) { ... }

    finally { ... }
   %>
   ```

   ​


2. ```java
   String msg_str = “”;
   String tmp = request.getParameter(“slf_msg_param_num”);
   tmp = StringUtil.isNullTrim(tmp);

   if (tmp.equals(“0”)) {
    msg_str = PropertyUtil.getValue(msg_id);
   } else {

    int param_ct = Integer.parseInt(tmp);
    String[] strArr = new String[param_ct];
    .......
   }
   ```

   ​


3. ```c
   void incorrect_password(const char *user) {
   	static const char msg_format[] = “%s cannot be authenticated.\n”;
    	size_t len = strlen(user) + sizeof(msg_format);
    	char *msg = (char *)malloc(len);
    	if (msg == NULL) {
   		 /* 오류 처리 */
    	}

   	int ret = snprintf(msg, len, msg_format, user);

    	if (ret < 0 || ret >= len) {
    		/* 오류 처리 */
    	}

    	fprintf(stderr, msg);
    	free(msg);
    	msg = NULL;
   }

   ```

   ​


4. ```java
   public void Test() throwsException {
    // dbsample : 84d5d0a08a3ec5e2d91a
    // 암호화 전, 후 : 1365ADMIN_01, aa84c40031d808196537ad3dcf81f9af
    String pwd = “aa84c40031d808196537ad3dcf81f9af”;
    String pwd1 = ARIAEngine.decARIA(pwd);
    System.out.println(pwd1);
   }
   ```



5. ```c
   umask(0);
   FILE *out = fopen("important_file", "w");
   if (out)
   {
   	fprintf(out, "secret\n");
   	fclose(out);
   }
   ```









