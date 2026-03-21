import * as Lark from "@larksuiteoapi/node-sdk";

// Test if we can get chat members to bypass app visibility restrictions
async function testChatMembers() {
  const client = new Lark.Client({
    appId: process.env.FEISHU_APP_ID || "",
    appSecret: process.env.FEISHU_APP_SECRET || "",
    appType: Lark.AppType.SelfBuild,
  });

  try {
    // 1. List all chats/groups
    console.log("=== Listing chats ===");
    const chatsResp: any = await client.im.chat.list({ params: { page_size: 100 } });
    console.log("Chats response:", JSON.stringify(chatsResp, null, 2));

    if (chatsResp.code === 0 && chatsResp.data?.items) {
      for (const chat of chatsResp.data.items.slice(0, 3)) {
        console.log(`\n=== Chat: ${chat.name} (${chat.chat_id}) ===`);
        
        // 2. Get chat members
        try {
          const membersResp: any = await client.im.chatMembers.get({
            path: { chat_id: chat.chat_id },
            params: { page_size: 100 }
          });
          console.log("Members response:", JSON.stringify(membersResp, null, 2));
        } catch (e: any) {
          console.log("Members error:", e.message);
        }
      }
    }

    // 3. Test search with different API
    console.log("\n=== Testing user search ===");
    const searchResp: any = await client.contact.user.list({ params: { page_size: 100 } });
    console.log("User list:", JSON.stringify(searchResp.data?.items?.map((u: any) => u.name), null, 2));

  } catch (e: any) {
    console.error("Error:", e.message);
  }
}

testChatMembers();
